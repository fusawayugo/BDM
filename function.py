def byte_to_acc(array):
    xyz=[]
    split_data = [array[i:i+2] for i in range(0, len(array), 2)]
    for data in split_data:
        value = int.from_bytes(data, byteorder='little', signed=True)
        xyz.append(value)
    return xyz

def byte_to_xacc(array):
    data=array[0:2]
    x=int.from_bytes(data, byteorder='little', signed=True)
    return x

'''
data = bytearray(b'\xf8\xff\xc8\xff\xd8\xfb')
xyz=byte_to_acc(data)
print(xyz)
'''
