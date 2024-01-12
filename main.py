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
                    #Aボタンを使う
                    a_data = button_service.get_characteristic(UUID_BUTTON_ASTATE)
                    async def change_A_STATE(sender,data):
                        global A_STATE
                        A_STATE=int.from_bytes(data)
                    await client.start_notify(a_data,change_A_STATE)
                    print('push A-button')
                    while True:
                        try:
                            if A_STATE>=1:
                                break
                            else:
                                await asyncio.sleep(0.03)
                        except KeyboardInterrupt:
                            await client.stop_notify(a_data)
                            break
                    
                    while True:
                        try:
                            if A_STATE==0:
                                break
                            else:
                                await asyncio.sleep(0.03)
                        except KeyboardInterrupt:
                            await client.stop_notify(a_data)
                            break
                if accelerometer_service:
                    data = await client.read_gatt_char(UUID_ACCELEROMETER_DATA)
                    initial_x,initial_y,initial_z=byte_to_acc(data)
                    initial_theta=np.arctan2(-initial_z,-initial_x)
                    while True:
                        try:
                            data = await client.read_gatt_char(UUID_ACCELEROMETER_DATA)
                            x,y,z=byte_to_acc(data)
                            asyncio.create_task(tan_scroll(x,z,initial_theta))
                            await asyncio.sleep(0.05)
                            if A_STATE!=0:
                                await client.stop_notify(a_data)
                                break
                        except KeyboardInterrupt:
                            await client.stop_notify(a_data)
                            #await client.stop_notify(data)
                            break  
                else:
                    print("service not found.")
                    await client.disconnect()
            except Exception as e:
                print(f"Error: {e}")
                await client.disconnect()
    else:
        print("Target device not found.")

if __name__ == "__main__":
    asyncio.run(main())