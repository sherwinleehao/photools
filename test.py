from photools import *
import time
# path = 'img'
path = '/Users/ws/Desktop/comparation/IMA'

files = getAllFiles(path)
# print(files)

st = time.time()

for file in files:
    iconPath = findThumb(file,"Temp/Cache")
    print(iconPath)

et = time.time()

print("Used time of %.3f"%(et-st))
