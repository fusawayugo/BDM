from bleak import BleakScanner, BleakClient
import asyncio
import pyautogui as pg
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from function import byte_to_acc,tan_scroll

target_address = "C2783BD9-2103-65E8-DF49-0F483733120E" 
target_address = "35B067D2-43F1-D6ED-2CC4-BA5761D51DB0"

UUID_ACCELEROMETER_SERVICE = "e95d0753-251d-470a-a062-fa1922dfa9a8"
UUID_ACCELEROMETER_DATA = "e95dca4b-251d-470a-a062-fa1922dfa9a8"

UUID_BUTTON_SERVICE =  "e95d9882-251d-470a-a062-fa1922dfa9a8"
UUID_BUTTON_ASTATE =  "e95dda90-251d-470a-a062-fa1922dfa9a8"
UUID_BUTTON_BSTATE =  "e95dda91-251d-470a-a062-fa1922dfa9a8"

A_STATE=0
LAST_A_STATE=0
B_STATE=0
SCROLL_ON=0

async def scroll(client):
    global SCROLL_ON
    init=1
    initial_theta=0
    while True: 
        try:
            data = await client.read_gatt_char(UUID_ACCELEROMETER_DATA)
            if SCROLL_ON:
                if init==1:
                    initial_x,initial_y,initial_z=byte_to_acc(data)
                    initial_theta=np.arctan2(-initial_z,-initial_x)
                    init=0
                else:
                    x,y,z=byte_to_acc(data)
                    asyncio.create_task(tan_scroll(x,z,initial_theta))
            else:
                init=1
            await asyncio.sleep(0.05)
        except Exception as e:
                print(f"Error: {e}")
    

async def main():
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

                accelerometer_service = None
                button_service = None
                s1=0
                for service in services:
                    if service.uuid == UUID_ACCELEROMETER_SERVICE:
                        accelerometer_service = service
                        s1+=1
                    elif service.uuid == UUID_BUTTON_SERVICE:
                        button_service = service
                        s1+=1
                    if s1==2:
                        break

                if button_service:
                    a_data = button_service.get_characteristic(UUID_BUTTON_ASTATE)
                    b_data = button_service.get_characteristic(UUID_BUTTON_BSTATE)
                    async def change_A_STATE(sender,data):
                        global A_STATE
                        global LAST_A_STATE
                        global SCROLL_ON
                        LAST_A_STATE=A_STATE
                        A_STATE=int.from_bytes(data)
                        if LAST_A_STATE>=1 and A_STATE==0:
                            if SCROLL_ON:
                                SCROLL_ON=0
                            else:
                                SCROLL_ON=1
                    async def change_B_STATE(sender,data):
                        global B_STATE
                        B_STATE=int.from_bytes(data)
                    await client.start_notify(a_data,change_A_STATE)
                    await client.start_notify(b_data,change_B_STATE)
                    print('push A-button to scroll')
                else:
                    print("button service not found.")
                    await client.disconnect()
                
                if accelerometer_service:
                    asyncio.create_task(scroll(client))
                    while True:
                        try:
                            await asyncio.sleep(0.1)
                        except KeyboardInterrupt:
                            break
                else:
                    print("acc service not found.")
                    await client.disconnect()
            except Exception as e:
                print(f"Error: {e}")
                await client.disconnect()
    else:
        print("Target device not found.")

if __name__ == "__main__":
    asyncio.run(main())