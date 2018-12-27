import cv2
from PIL import Image, ImageDraw, ExifTags
import numpy as np
import time
from photools import *


def getUnmult1(im):
    b, g, r, a = cv2.split(im)
    _, thresh = cv2.threshold(a, 0, 255, cv2.THRESH_BINARY)
    nA = thresh / 255
    nB = (b / 255) * (thresh / 255)
    nG = (g / 255) * (thresh / 255)
    nR = (r / 255) * (thresh / 255)
    umIma = cv2.merge([nB * 255, nG * 255, nR * 255, nA * 255])
    dst = umIma.astype(np.uint8)
    return dst


def getUnmult2(im):
    b, g, r, a = cv2.split(im)
    _, thresh = cv2.threshold(a, 0, 255, cv2.THRESH_BINARY)
    nT = thresh / 255
    nA = a / 255
    nB = (b / 255) / nA * nT
    nG = (g / 255) / nA * nT
    nR = (r / 255) / nA * nT
    umIma = cv2.merge([nB * 255, nG * 255, nR * 255, nT * 255])
    where_are_nan = np.isnan(umIma)
    umIma[where_are_nan] = 0
    dst = umIma.astype(np.uint8)
    return dst


def getExpansionEdge(ima, val):
    umIma = getUnmult1(ima)

    blurIma = cv2.blur(umIma, (val, val))
    # blurIma = cv2.medianBlur(umIma,5)

    umBlurIma = getUnmult2(blurIma)

    _, _, _, a = cv2.split(umIma)
    newa = 1 - (a / 255)
    bb, gg, rr, aa = cv2.split(umBlurIma)
    BG = cv2.merge([bb * newa, gg * newa, rr * newa, aa * newa])
    BG = BG.astype(np.uint8)
    final = umIma + BG

    return final


def getDraftExpansion(ima, val, sample):
    _, _, _, a = cv2.split(ima)
    ret, thresh1 = cv2.threshold(a, 0, 255, cv2.THRESH_BINARY)
    mask = 255 - thresh1
    miniIma = cv2.resize(ima, None, fx=(1 / sample), fy=(1 / sample), interpolation=cv2.INTER_NEAREST)
    blurIma = cv2.blur(miniIma, (val, val))
    umBlurIma = getUnmult2(blurIma)
    bigIma = cv2.resize(umBlurIma, None, fx=sample, fy=sample, interpolation=cv2.INTER_NEAREST)
    masked = cv2.bitwise_and(bigIma, bigIma, mask=mask)
    dst = cv2.add(masked, ima)
    return dst


def getOffsetMerge(ima, x, y):
    dst = getUnmult1(ima)
    _, _, _, a = cv2.split(dst)
    matte = 1 - (a / 255)
    # dst = getExpansion(dst,4)
    # h,w,_ = dst.shape
    # print(h,w)
    # dst[5:,5:] = dst[:-5,:-5]

    temp = dst[:-y, :-x]
    tB, tG, tR, tA = cv2.split(temp)
    nMatte = matte[y:, x:]
    nB = tB * nMatte
    nG = tG * nMatte
    nR = tR * nMatte
    nA = tA * nMatte

    new = cv2.merge([nB, nG, nR, nA])
    new = new.astype(np.uint8)
    dst[y:, x:] += new

    return dst


def getEmptyFill(ima):
    st = time.time()
    for i in range(1):
        ima = getExpansionEdge(ima, 4)
    # for i in range(10):
    #     ima = getDraftExpansion(ima,4,2)
    # for i in range(20):
    #     ima = getDraftExpansion(ima,4,4)
    dst = ima
    et = time.time()
    print("Fill Empty Using %.3f" % (et - st))
    return dst


def saveAlphaInGreen(im, path):
    b, g, r, a = cv2.split(im)
    b[:][:] = 0
    dst = cv2.merge([b, a, b])
    cv2.imwrite(path, dst)


def getValueROI(path):
    sample = 8

    def getNotZero(list, multi):
        start = 0
        end = len(list)
        for i in range(len(list)):
            if list[i] == 0:
                pass
            else:
                start = i
                break
        for j in range(len(list)):
            if list[-j] == 0:
                pass
            else:
                end = len(list) - j
                break
        return (start - 1) * multi, (end + 1) * multi

    img = cv2.imread(path, -1)
    B, G, R, A = cv2.split(img)
    ret, thresh1 = cv2.threshold(A, 0, 255, cv2.THRESH_BINARY)
    mini = cv2.resize(thresh1, None, fx=(1 / sample), fy=(1 / sample), interpolation=cv2.INTER_NEAREST)
    h, w = mini.shape
    horizontal = []
    vertical = []
    for i in range(w):
        temp = mini[0:h, i]
        horizontal.append(np.sum(temp))
    for i in range(h):
        temp = mini[i, 0:w]
        vertical.append(np.sum(temp))
    hs, he = getNotZero(horizontal, sample)
    vs, ve = getNotZero(vertical, sample)
    # roi = thresh1[vs:ve,hs:he]
    return vs, ve, hs, he


def getSeqROI(path):
    st = time.time()
    files = getAllFiles(path)
    vss = []
    ves = []
    hss = []
    hes = []
    for file in files:
        if '.png' in file:
            vs, ve, hs, he = getValueROI(file)
            vss.append(vs)
            ves.append(ve)
            hss.append(hs)
            hes.append(he)
    vs = min(vss)
    ve = max(ves)
    hs = min(hss)
    he = max(hes)
    et = time.time()
    print("Using %.3f to finish" % (et - st))
    return vs, ve, hs, he

def getEdgeKeyColor(path):
    from collections import Counter
    im = cv2.imread(path, -1)
    im = getUnmult1(im)
    sample = 4
    im = cv2.resize(im, None, fx=(1 / sample), fy=(1 / sample), interpolation=cv2.INTER_NEAREST)
    _, _, _, a = cv2.split(im)
    h, w, _ = im.shape
    canny = cv2.Canny(a, 50, 150, apertureSize=5)
    im = getExpansionEdge(im, 4)
    edgeColors = []
    for y in range(h):
        for x in range(w):
            if canny[y][x] != 0:
                edgeColors.append(str(im[y][x].tolist()))
    result = Counter(edgeColors)
    color = result.most_common(1)[0][0][1:-1].split(', ')
    return int(color[0]),int(color[1]),int(color[2]),int(color[3])

def getSolidColor(b,g,r,h,w,d):
    img = np.zeros([h, w, d], np.uint8)
    img[:, :, 0] = np.ones([h, w])* b
    img[:, :, 1] = np.ones([h, w])* g
    img[:, :, 2] = np.ones([h, w])* r
    return img

def initTga(path):
    mkdir(path)
    files = getAllFiles(path)
    for file in files:
        os.remove(file)



def getAlphaBlend(ima,imb,premult):
    if ima.shape == imb.shape:
        _,_,_,a = cv2.split(ima)
        a = a.astype(np.float)/255
        h,w,d = ima.shape
        if d ==3:
            alpha = cv2.merge([a,a,a])
        else:
            alpha = cv2.merge([a, a, a, a])
        matte = 1 - alpha
        if premult:
            FG = ima.astype(np.float)
        else:
            FG = ima.astype(np.float) * alpha
        BG = imb.astype(np.float) * matte
        dst = FG + BG
        return dst

    else:
        print("Please check about the two IMGs channels.")


def saveSeqROI(path, tga):
    initTga(tga)
    vs, ve, hs, he = getSeqROI(path)
    print("Get Seq ROI of:", vs, ve, hs, he, '\n')

    files = getAllFiles(path)
    for file in files:
        if '.png' in file:
            straight_name = 'Str_' + os.path.basename(file)
            aplha_Name = 'Alp_' + os.path.basename(file)

            straight_path = os.path.join(tga, straight_name)
            aplha_path = os.path.join(tga, aplha_Name)
            im = cv2.imread(file, -1)
            ROI_im = im[vs:ve, hs:he]
            saveAlphaInGreen(ROI_im, aplha_path)
            dst = getEmptyFill(ROI_im)
            cv2.imwrite(straight_path, dst)
            print("Finish saving %s" % os.path.basename(file))

    cmd_Str = 'ffmpeg -r 25 -i C:\Python\photools\Temp\EXP\Str_test_%05d.png  -b:v 3000K -vcodec h264  -pix_fmt yuv420p C:\Python\photools\Temp\EXP\Str_test.mp4'
    cmd_Alp = 'ffmpeg -r 25 -i C:\Python\photools\Temp\EXP\Alp_test_%05d.png  -b:v 3000K -vcodec h264  -pix_fmt yuv420p C:\Python\photools\Temp\EXP\Alp_test.mp4'
    os.system(cmd_Str)
    os.system(cmd_Alp)


def main():
    st = time.time()

    path = r'C:\Python\photools\Temp\PNG'
    tga = r'C:\Python\photools\Temp\EXP'
    saveSeqROI(path, tga)

    et = time.time()
    print("Using %.3f to finish" % (et - st))

def main2():
    path = r'Temp\ROII\test_00001.png'
    path1 = r'Temp\ROII\test_path1.png'
    path2 = r'Temp\ROII\test_path2.png'

    im = cv2.imread(path,-1)
    sample = 2
    im = cv2.resize(im, None, fx=(1 / sample), fy=(1 / sample), interpolation=cv2.INTER_NEAREST)
    im = getUnmult1(im)
    val =20
    # blurIma = cv2.blur(im, (val, val))
    blurIma = im
    b,g,r,a = cv2.split(blurIma)
    im = cv2.merge([b,g,r])
    h,w,d = im.shape
    solid = getSolidColor(0,255,0,h,w,d)
    mask = 1-(a/255)
    # dst = cv2.multiply(solid,a)

    alpha = cv2.merge([a,a,a])
    print(im[150][600])

    foreground = im.astype(float)
    background = solid.astype(float)
    alpha = alpha.astype(float) / 255
    matte = 1-alpha

    print(foreground.dtype)
    print(foreground[150][600])

    foreground = cv2.multiply(alpha, foreground)
    background = cv2.multiply(matte, background)
    outImage = cv2.add(foreground, background)
    print(foreground.dtype)
    print(foreground[150][600])


    cv2.imshow('XXX',outImage)
    cv2.waitKey(0)

    # cv2.imshow('xxx',edge)
    # cv2.waitKey(0)

def main3():
    path = r'Temp\ROII\test_00001.png'
    im = cv2.imread(path,-1)
    sample = 2
    blurVal =5
    im = cv2.resize(im, None, fx=(1 / sample), fy=(1 / sample), interpolation=cv2.INTER_NEAREST)
    im = getUnmult1(im)
    im = cv2.blur(im, (blurVal, blurVal))
    h,w,d = im.shape
    solid = getSolidColor(0,255,0,h,w,d)
    dst = getAlphaBlend(im,solid,1)
    cv2.imshow('dst',dst/255)
    cv2.waitKey(0)

if __name__ == '__main__':
    # path = r'Temp/Test_fill_hole.png'
    # getBeautyLayer(path)
    # getValueROI(path)
    # main()
    main3()
