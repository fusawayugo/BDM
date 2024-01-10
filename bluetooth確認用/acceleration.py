from bleak import BleakScanner, BleakClient
import asyncio
import pyautogui as pg
import sys
import matplotlib.pyplot as plt
from time import sleep


sys.path.append('../')
from function import byte_to_xacc


async def scroll(x):
    a_sc=-(x+1000)/200
    if abs(a_sc)>1:
        pg.scroll(int(a_sc))
        print(a_sc,int(a_sc))
    pass



target_address = "C2783BD9-2103-65E8-DF49-0F483733120E" 
# target_address = "35B067D2-43F1-D6ED-2CC4-BA5761D51DB0" # 加速度データを持つデバイスのMACアドレス



UUID_ACCELEROMETER_SERVICE = "e95d0753-251d-470a-a062-fa1922dfa9a8"
UUID_ACCELEROMETER_DATA = "e95dca4b-251d-470a-a062-fa1922dfa9a8"

UUID_BUTTON_SERVICE =  "e95d9882-251d-470a-a062-fa1922dfa9a8"
UUID_BUTTON_ASTATE =  "e95dda90-251d-470a-a062-fa1922dfa9a8"
UUID_BUTTON_BSTATE =  "e95dda91-251d-470a-a062-fa1922dfa9a8"


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

                accelerometer_service = None
                for service in services:
                    if service.uuid == UUID_ACCELEROMETER_SERVICE:
                        accelerometer_service = service
                        break

                if accelerometer_service:
                    '''
                    data_char = accelerometer_service.get_characteristic(UUID_ACCELEROMETER_DATA)

                    async def acceleration_handler(sender, data):
                        x=byte_to_xacc(data)
                        # Process acceleration data here  
                        #print(f"Acceleration: X={x}, Y={y}, Z={z},count={input_count}")
                        await scroll(x)
                    
                    await client.start_notify(data_char, acceleration_handler)

                    while True:
                        try:
                            await asyncio.sleep(1)
                        except KeyboardInterrupt:
                            await client.stop_notify(data_char)
                            break
                    '''
                    while True:
                        try:
                            data = await client.read_gatt_char(UUID_ACCELEROMETER_DATA)
                            x=byte_to_xacc(data)
                            asyncio.create_task(scroll(x))
                            sleep(0.05)
                        except KeyboardInterrupt:
                            await client.stop_notify(data)
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


