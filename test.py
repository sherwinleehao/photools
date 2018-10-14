from PIL import ImageGrab
import numpy
import cv2
import time
im = ImageGrab.grab()
im = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
im.save('Temp/Test.png','png')

global oldImg
global oldTime
oldTime =time.time()


def isUpdated(newImg):
    isupdate = False
    deltaValue = 0
    deltaTime = 0
    global oldImg
    global oldTime
    nImg = cv2.resize(newImg, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_NEAREST)
    try:
        matte = nImg - oldImg
        matte_gray = cv2.cvtColor(matte, cv2.COLOR_BGR2GRAY)
        deltaValue = sum(sum(matte_gray))
        print("detalValue :",deltaValue)
    except:
        pass

    oldImg = nImg
    if deltaValue >100:
        isupdate = True
        deltaTime = time.time()-oldTime
        oldTime = time.time()

    return isupdate,deltaTime

ot = time.time()
for i in range(1000):
    im = ImageGrab.grab(bbox=(0, 0, 10, 10))
    # im.save('Temp/Test.png', 'png')
    img = cv2.cvtColor(numpy.asarray(im), cv2.COLOR_RGB2BGR)
    print(isUpdated(img))
    ut = time.time()-ot
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  %.3f"%(1/ut))
    ot = time.time()


    # cv2.imshow("crop", img)
    # print(img[1][1])