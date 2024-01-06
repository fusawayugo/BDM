from bleak import BleakScanner, BleakClient
import asyncio

target_address = "C2783BD9-2103-65E8-DF49-0F483733120E"  # 加速度データを持つデバイスのMACアドレス

UUID_ACCELEROMETER_SERVICE = "e95d0753-251d-470a-a062-fa1922dfa9a8"
UUID_ACCELEROMETER_DATA = "e95dca4b-251d-470a-a062-fa1922dfa9a8"

async def get_acceleration():
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

                # print("Services available:")
                # for service in services:
                #     print(service)

                accelerometer_service = None
                for service in services:
                    if service.uuid == UUID_ACCELEROMETER_SERVICE:
                        accelerometer_service = service
                        break

                if accelerometer_service:
                    data_char = accelerometer_service.get_characteristic(UUID_ACCELEROMETER_DATA)

                    def acceleration_handler(sender, data):
                        x = data[0]  # Assuming data format is [x, y, z] bytes
                        y = data[1]
                        z = data[2]
                        # Process acceleration data here
                        print(f"Acceleration: X={x}, Y={y}, Z={z}")

                    await client.start_notify(data_char, acceleration_handler)

                    while True:
                        try:
                            await asyncio.sleep(1)
                        except KeyboardInterrupt:
                            await client.stop_notify(data_char)
                            break

                else:
                    print("Accelerometer service not found.")
                    await client.disconnect()
            except Exception as e:
                print(f"Error: {e}")
                await client.disconnect()
    else:
        print("Target device not found.")

if __name__ == "__main__":
    asyncio.run(get_acceleration())
