from bleak import BleakScanner, BleakClient
import asyncio
import pyautogui as pg
import sys
import matplotlib.pyplot as plt
from time import sleep

#target_address = "C2783BD9-2103-65E8-DF49-0F483733120E" 
target_address = "35B067D2-43F1-D6ED-2CC4-BA5761D51DB0"


UUID_BUTTON_SERVICE =  "e95d9882-251d-470a-a062-fa1922dfa9a8"
UUID_BUTTON_ASTATE =  "e95dda90-251d-470a-a062-fa1922dfa9a8"
UUID_BUTTON_BSTATE =  "e95dda91-251d-470a-a062-fa1922dfa9a8"


async def get_button():
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

                button_service = None
                for service in services:
                    if service.uuid == UUID_BUTTON_SERVICE:
                        button_service = service
                        break

                if button_service:

                    
                    while True:
                        try:
                            a_data = await client.read_gatt_char(UUID_BUTTON_ASTATE)
                            b_data = await client.read_gatt_char(UUID_BUTTON_BSTATE)
                            print(a_data,b_data)
                            sleep(0.05)
                        except KeyboardInterrupt:
                            #await client.stop_notify(data)
                            break  
                    
                else:
                    print("button service not found.")
                    await client.disconnect()
            except Exception as e:
                print(f"Error: {e}")
                await client.disconnect()
    else:
        print("Target device not found.")

if __name__ == "__main__":
    asyncio.run(get_button())
