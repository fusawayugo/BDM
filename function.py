import asyncio
import pyautogui as pg
import numpy as np

def byte_to_acc(array):
    xyz=[0,0,0]
    split_data = [array[i:i+2] for i in range(0, len(array), 2)]
    for i in range(3):
        value = int.from_bytes(split_data[i], byteorder='little', signed=True)
        xyz[i]=value
    xyz=tuple(xyz)
    return xyz

def byte_to_xacc(array):
    data=array[0:2]
    x=int.from_bytes(data, byteorder='little', signed=True)
    return x


async def scroll(x,z,theta0):
    theta=np.arctan2(-z,-x)
    pg.scroll((theta-theta0)*3)


