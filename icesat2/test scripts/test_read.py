#!/usr/bin/env python
import h5py
import numpy as np 
from PIL import Image

#put the actual file name here
filename = 'GLAH01_033_2129_002_0178_1_02_0001.H5'

f = h5py.File(filename, 'r')

for key in f.keys():
    print(key)

group = f[key]

for key in group.keys():
    data = group[key][:]
    if(key == "Image_00"):
        img = Image.fromarray(data.astype('uint8'), 'RGB')
        img.save('plxwerk', 'JPEG')
        img.show()
    print(data)


f.close()

