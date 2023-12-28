import asyncio
from bleak import BleakScanner, BleakClient

async def scan_and_get_uuids():
    async with BleakScanner() as scanner:
        devices = await scanner.discover()
        for device in devices:
            #print(f"Device name: {device.name} / Device address: {device.address}")
            if device.address=="35B067D2-43F1-D6ED-2CC4-BA5761D51DB0":
                async with BleakClient(device) as client:
                    services = await client.get_services()
                    for service in services:
                        print(f"Service UUID: {service.uuid}")
                        characteristics = service.characteristics
                        for char in characteristics:
                            print(f"Characteristic UUID: {char.uuid}")


if __name__ == "__main__":
    #ADDRESS_TO_SCAN = "XX:XX:XX:XX:XX:XX"  # ここにスキャンしたいデバイスのMACアドレスを入力してください。
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scan_and_get_uuids())
