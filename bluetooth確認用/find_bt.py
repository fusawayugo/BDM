import asyncio
from bleak import discover

async def discover_devices():
    devices = await discover()
    for device in devices:
        print(f"Device name: {device.name} / Device address: {device.address}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(discover_devices())
