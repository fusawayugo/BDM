from bleak import BleakScanner, BleakClient
import asyncio
import platform


# 接続先のmicro:bitデバイスのUUID
target_address = "C2783BD9-2103-65E8-DF49-0F483733120E"  # 接続したいデバイスのMACアドレス

# サービスおよびキャラクタリスティックのUUID
UUID_TEMPERATURE_SERVICE = "e95d6100-251d-470a-a062-fa1922dfa9a8"
UUID_TEMPERATURE_CHARACTERISTIC_DATA = "e95d9250-251d-470a-a062-fa1922dfa9a8"
UUID_TEMPERATURE_CHARACTERISTIC_PERIOD = "e95d1b25-251d-470a-a062-fa1922dfa9a8"

# 取得間隔（ミリ秒）
INTERVAL = bytearray([0x64, 0x00])  # 100ミリ秒（0x0064をリトルエンディアンで指定）

async def get_temperature():
    scanner = BleakScanner()
    devices = await scanner.discover()

    target_device = None
    for device in devices:
        if device.address.upper() == target_address.upper():
            target_device = device
            break

    if target_device:
        async with BleakClient(target_device) as client:
            try:
                await client.connect()
                services = client.services

                print("Services available:")
                for service in services:
                    print(service)

                services = client.services
                temperature_service = None
                for service in services:
                    if service.uuid == UUID_TEMPERATURE_SERVICE:
                        temperature_service = service
                        break

                if temperature_service:
                    period_char = temperature_service.get_characteristic(UUID_TEMPERATURE_CHARACTERISTIC_PERIOD)
                    await client.write_gatt_char(period_char, INTERVAL, response=True)

                    data_char = temperature_service.get_characteristic(UUID_TEMPERATURE_CHARACTERISTIC_DATA)

                    def temperature_handler(sender, data):
                        temperature_value = int.from_bytes(data, byteorder="little")
                        print(f"Temperature: {temperature_value}℃")

                    await client.start_notify(data_char, temperature_handler)

                    while True:
                        try:
                            await asyncio.sleep(1)
                        except KeyboardInterrupt:
                            await client.stop_notify(data_char)
                            break

                else:
                    print("Temperature service not found.")
                    await client.disconnect()
            except Exception as e:
                print(f"Error: {e}")
                await client.disconnect()
    else:
        print("Target device not found.")

if __name__ == "__main__":
    asyncio.run(get_temperature())
