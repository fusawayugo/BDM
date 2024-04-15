import asyncio
from bleak import BleakScanner, BleakClient, discover

async def scan_and_get_uuids():
    devices = await discover()
    for device in devices:
        print(f"Device name: {device.name} / Device address: {device.address}")
        if device.address=="CD:AD:38:E5:14:4A":
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
