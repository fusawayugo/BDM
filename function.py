import asyncio
import pyautogui as pg
import numpy as np
import pywinctl as pwc

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


async def tan_scroll(x,z,theta0):
    theta=np.arctan2(-z,-x)
    a=0
    if theta-theta0<-np.pi:
        a=2*np.pi
    elif theta-theta0>np.pi:
        a=-2*np.pi
    sc=int((theta-theta0+a)*4)
    pg.scroll(sc)

async def tan_mag_shr(x,z,theta0):
    theta=np.arctan2(-z,-x)
    a=0
    if theta-theta0<-np.pi:
        a=2*np.pi
    elif theta-theta0>np.pi:
        a=-2*np.pi
    ms=theta-theta0+a
    if ms>np.pi/5:
        pg.hotkey('command','shift',';')
        #拡大できない
    elif ms<-np.pi/5:
        pg.hotkey('command','-')

def calc_norm(x,y,z):
    norm=np.linalg.norm(np.array([x,y,z]))
    #print(norm)
    return norm


async def delete_window():
    '''
    window=pwc.getActiveWindow()
    print(window)
    window.close()
    '''
    pg.hotkey('command','w')




