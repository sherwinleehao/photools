import os
import PIL
from PIL import Image, ImageDraw
import time
from pydub import AudioSegment
import math
import hashlib

def getAllFiles(path):
    tempfiles = []
    for i in os.listdir(path):
        tempPath = os.path.join(path, i)
        if os.path.isfile(tempPath):
            tempfiles.append(tempPath)
        else:
            tempfiles += getAllFiles(tempPath)
    return tempfiles

def getDraftMD5(filePath):
    tempInfo = ''
    fsize = os.path.getsize(filePath)
    mt = os.path.getmtime(filePath)
    tempInfo += str(fsize)
    tempInfo += str(mt)

    hash_md5 = hashlib.md5()
    hash_md5.update(tempInfo.encode())
    return hash_md5.hexdigest()

def getWaveform(filePath,width,height):
    sound = AudioSegment.from_file(filePath, format="mp3")
    step = len(sound)/width
    wave = []
    for i in range(0, width):
        segment = sound[i*step:(i+1)*step]
        wave.append(segment.max)
    waveform = Image.new('RGB',(width,height),(21, 96, 67))
    draw = ImageDraw.Draw(waveform)
    for i in range(len(wave)):
        value = height*(wave[i]/32768)
        sp = (height-value)/2
        draw.line((i,sp,i,value+sp),fill=(37, 208, 141))
    del draw
    return waveform


def saveWaveform(filePath,tgaPath,width,height):
    waveform = getWaveform(filePath,width,height)
    waveform.save(tgaPath)
    waveform.close()

def findWaveform(filePath):
    MD5 = getDraftMD5(filePath)
    tgaPath = os.path.join(r'/Users/ws/Python/photools/Temp/Cache/%s.png'%str(MD5))
    if os.path.exists(tgaPath):
        return tgaPath
    else:
        saveWaveform(filePath,tgaPath,512,128)
        return tgaPath


if __name__ == '__main__':
    st = time.time()

    path = r'/Users/ws/Music'

    files = getAllFiles(path)
    for i in files:

        if ".mp3" in i:
            print(i)
            print(findWaveform(i))


    et = time.time()
    print("Used time :",(et-st))