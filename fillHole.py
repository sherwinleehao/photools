import cv2
from PIL import Image, ImageDraw, ExifTags
import numpy as np
import time
from photools import *


def getBeautyLayer(path):
    st = time.time()

    img = cv2.imread(path, -1)
    h, w, _ = img.shape
    B, G, R, A = cv2.split(img)
    ret, thresh1 = cv2.threshold(A, 0, 255, cv2.THRESH_BINARY)
    nB = (B / 255) * (thresh1 / 255)
    nG = (G / 255) * (thresh1 / 255)
    nR = (R / 255) * (thresh1 / 255)
    nA = thresh1 / 255
    cv2.namedWindow("Image")
    # newImg = cv2.merge([nB, nG, nR])
    newImg = cv2.merge([nB, nG, nR, nA])

    def getNearestValueIndex(data):
        for i in range(len(data)):
            if data[i] != 0:
                return i

    def getIndex(data):
        index = getNearestValueIndex(data)
        if index is None:
            return 100000
        else:
            return index

    def getNearestColor(x, y, w, h, im, alpha):
        line0 = alpha[0:y, x]  # checked
        line1 = alpha[y, x:w]  # checked
        line2 = alpha[y:h, x]  # checked
        line3 = alpha[y, 0:x]  # checked

        index0 = getIndex(line0)
        index1 = getIndex(line1)
        index2 = getIndex(line2)
        index3 = getIndex(line3)
        indexs = [index0, index1, index2, index3]
        index = min(indexs)

        if index0 == index1 == index2 == index3:
            val = im[y][x]
        else:
            if index0 == index:
                val = im[y - index0][x]
                # print(val)
            elif index1 == index:
                val = im[y][x + index1]
                # print(val)
            elif index2 == index:
                val = im[y + index2][x]
                # print(val)
            elif index3 == index:
                val = im[y][x - index3]
                # print(val)

        return val
        # im[0:y, x] = (0,0,1.0)
        # im[y, x:w] = (0,0,1.0)
        # im[y:h,x] = (0,0,1.0)
        # im[y,0:x] = (0,0,1.0)
        # return im

    # for x in range(w):
    #     for y in range(h):
    #         if thresh1[y][x] == 0:
    #             newImg[y][x] = getNearestColor(x, y, w, h, newImg, thresh1)

    # print(thresh1[120][0:150])
    # newImg[120][0:150]= (0,0,1.0)

    # newImg = getNearestColor(130, 100, w, h,newImg ,thresh1)

    # print("New Image dtype",newImg.dtype)
    # img = np.array(newImg*255, dtype=np.uint8)
    # cv2.imwrite(r'Temp/Test_fill_hole2.png',newImg)
    # cv2.imshow("Image", newImg)

    def expansionEdge(ima, val):
        b, g, r, a = cv2.split(ima)
        dst = cv2.blur(ima, (val, val))
        B, G, R, A = cv2.split(dst)
        ret, threshA = cv2.threshold(A, 0, 1, cv2.THRESH_BINARY)

        nA = threshA * (1 - a)
        nB = B/A*nA
        nG = G/A*nA
        nR = R/A*nA
        ndst = cv2.merge([nB, nG, nR, nA])

        where_are_nan = np.isnan(ndst)
        ndst[where_are_nan] = 0

        final = ndst + ima
        return final

    def getExpansion(ima, levels):
        for i in range(2,levels):
            # ima = expansionEdge(ima,int(pow(1.3,i)) )
            ima = expansionEdge(ima,8)
        return ima

    dst = getExpansion(newImg, 20)
    print(dst.shape)
    et = time.time()
    print("Draw the image in %.3f" % (et - st))
    cv2.imshow("Image", dst)
    cv2.waitKey(0)

def saveAlphaInGreen(im,path):
    b, g, r, a = cv2.split(im)
    b[:][:] = 0
    print(a[200][200])
    dst = cv2.merge([b, a, b])
    cv2.imwrite(path,dst)

def getValueROI(path):
    sample = 8
    def getNotZero(list,multi):
        start = 0
        end = len(list)
        for i in range(len(list)):
            if list[i] == 0 :
                pass
            else:
                start = i
                break
        for j in range(len(list)):
            if list[-j] == 0:
                pass
            else:
                end = len(list)-j
                break
        return (start-1)*multi,(end+1)*multi

    img = cv2.imread(path, -1)
    B, G, R, A = cv2.split(img)
    ret, thresh1 = cv2.threshold(A, 0, 255, cv2.THRESH_BINARY)
    mini = cv2.resize(thresh1, None, fx=(1/sample), fy=(1/sample), interpolation=cv2.INTER_NEAREST)
    h,w = mini.shape
    horizontal = []
    vertical = []
    for i in range(w):
        temp = mini[0:h,i]
        horizontal.append(np.sum(temp))
    for i in range(h):
        temp = mini[i,0:w]
        vertical.append(np.sum(temp))
    hs,he = getNotZero(horizontal,sample)
    vs,ve = getNotZero(vertical,sample)
    # roi = thresh1[vs:ve,hs:he]
    return vs,ve,hs,he

def getSeqROI(path):
    st = time.time()
    files = getAllFiles(path)
    vss=[]
    ves=[]
    hss=[]
    hes=[]
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

def saveSeqROI(path):
    vs, ve, hs, he = getSeqROI(path)
    st = time.time()
    files = getAllFiles(path)
    for file in files:
        if '.png' in file and 'ROI_' not in file:
            name = 'ROI_'+os.path.basename(file)
            aplhaName = 'Alp_'+os.path.basename(file)
            folder = os.path.dirname(file)
            newFolder = os.path.join(folder,'ROI')
            mkdir(newFolder)
            tga = os.path.join(newFolder,name)
            tga2 = os.path.join(newFolder,aplhaName)
            im = cv2.imread(file,-1)
            saveAlphaInGreen(im,tga2)
            nim = im[vs:ve, hs:he]
            cv2.imwrite(tga, nim)
            print("Finish saving %s" % name)

    et = time.time()
    print("Using %.3f to finish" % (et - st))

def main():
    path = r'C:\Users\ws\Desktop\PNG'
    # print(getSeqROI(path))
    saveSeqROI(path)


def main2():
    path = r'C:\Users\ws\Desktop\PNG\ROI\test_00006.png'
    path1 = r'C:\Users\ws\Desktop\PNG\ROI\test_0.png'
    path2 = r'C:\Users\ws\Desktop\PNG\ROI\test_1.png'
    im = cv2.imread(path,-1)
    saveAlphaInGreen(im, path2)

if __name__ == '__main__':
    path = r'Temp/Test_fill_hole.png'
    # getBeautyLayer(path)
    # getValueROI(path)
    main()
    # main2()