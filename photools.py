#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Image Tool Library

Author: Sherwin Lee
Website: Sherwinleehao.com
Last edited: 20180828
"""

import os
import cv2
import time
from PIL import Image, ImageDraw, ExifTags
import rawpy
import imageio
import exifread
import io
import uuid
import filetype
import queue
import threading
from multiprocessing import Pool
import json
import ffmpy
import subprocess
import numpy
import zipfile
import hashlib


def getPhotoROIs(path, level, size):
    blockSize = size
    im = cv2.imread(path)
    height, width, _ = im.shape
    res = []
    # # im = cv2.resize(im, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_CUBIC)
    # r = [10,120,123,134]
    # # ROI 逻辑是左上角x,y,roi_w,roi,w
    # imCrop = im[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
    #
    # imgName = r"Images\%.03f.png"%time.time()
    # # cv2.imshow("Image", imCrop)
    # cv2.imwrite(imgName, imCrop)
    # # cv2.waitKey(0)

    for x in range(level + 1):
        for y in range(level + 1):
            # print("Block :", x, y)
            detalX = (width - blockSize) / level
            detalY = (height - blockSize) / level

            blockPosX = int(x * detalX + (blockSize / 2))
            blockPosY = int(y * detalY + (blockSize / 2))
            # print(blockPosX, blockPosY)
            r = [blockPosX - (blockSize / 2), blockPosY - (blockSize / 2), blockSize, blockSize]
            # print(r)
            imCrop = im[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
            # imgName = r"images\temp\IMG_%d_%d.png" % (y, x)
            # cv2.imwrite(imgName, imCrop)
            res.append(imCrop)
    return res


def detectBlur(ima):
    # image = cv2.imread(ima)
    image = ima
    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    return imageVar


def detectFaces(img, scale):
    # img = cv2.imread(image_name)
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    face_cascade = cv2.CascadeClassifier(r"haarcascade_frontalface_default.xml")
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img  # if语句：如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # 1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变
    # result = []
    # for (x,y,width,height) in faces:
    #     result.append((x,y,x+width,y+height))
    # print(result)
    # print("Find %d faces in the image."%len(result))
    # return result
    return faces


def getAllFiles(path):
    tempfiles = []
    for i in os.listdir(path):
        tempPath = os.path.join(path, i)
        if os.path.isfile(tempPath):
            tempfiles.append(tempPath)
            # print("Append Path:",tempPath)
        else:
            tempfiles += getAllFiles(tempPath)
    return tempfiles


def getResizedImg(frame, limit):
    frameSize = frame.size
    if frameSize[0] > frameSize[1]:
        size = frameSize[0]
    else:
        size = frameSize[1]

    imgScale = limit / size
    thumbSize = (int(frameSize[0] * imgScale), int(frameSize[1] * imgScale))
    thumb = frame.resize(thumbSize, resample=1)
    return thumb


def getImgExif(filePath):
    path = filePath
    img = Image.open(path)
    exif = {
        ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in ExifTags.TAGS
    }
    return exif


def getRawExif(filePath):
    f = open(filePath, 'rb')
    tags = exifread.process_file(f)
    return tags


def getThumbnail(filePath, frameSize):
    if os.path.isfile(filePath):
        try:
            exif = getRawExif(filePath)
            thumb = exif['JPEGThumbnail']

            stream = io.BytesIO(thumb)
            img = Image.open(stream)
            rota = "Horizontal (normal)"
            try:
                rota = str(exif['Image Orientation'])
            except:
                pass
            # print(rota)
            if "Horizontal" in rota:
                out = img
                thumb = getResizedImg(out, frameSize)
                return thumb
            else:
                if "180" in rota:
                    out = img.transpose(Image.ROTATE_180)
                    thumb = getResizedImg(out, frameSize)
                    return thumb
                if "CCW" in rota:
                    out = img.transpose(Image.ROTATE_90)
                    thumb = getResizedImg(out, frameSize)
                    return thumb
                else:
                    out = img.transpose(Image.ROTATE_270)
                    thumb = getResizedImg(out, frameSize)
                    return thumb
        except:
            print("Sorry---Can't find its EXIF  ")
            img = Image.open(filePath)
            thumb = getResizedImg(img, frameSize)
            return thumb


def getMediaInfo(filePath):
    tup_resp = ffmpy.FFprobe(
        inputs={filePath: None},
        global_options=[
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format', '-show_streams']
    ).run(stdout=subprocess.PIPE)
    meta = json.loads(tup_resp[0].decode('utf-8'))
    print(meta)
    return meta


def getMD5(filePath):
    hash_md5 = hashlib.md5()
    with open(filePath, 'rb')as f:
        for chunk in iter(lambda: f.read(1024 * 8), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def getDraftMD5(filePath):
    tempInfo = ''
    fsize = os.path.getsize(filePath)
    mt = os.path.getmtime(filePath)
    tempInfo += str(fsize)
    tempInfo += str(mt)

    hash_md5 = hashlib.md5()
    hash_md5.update(tempInfo.encode())
    return hash_md5.hexdigest()


def getVideoFrame(filePath, frameSize, frameID):
    image = None
    cap = cv2.VideoCapture(filePath)
    # while (cap.isOpened()):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frameID)
    ret, frame = cap.read()
    width, height, _ = frame.shape
    if width > height:
        scale = frameSize / width
    else:
        scale = frameSize / height
    frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    cap.release()
    return image


def getVideoFrames(filePath, frameSize, frameCount):
    image = None
    frames = []
    cap = cv2.VideoCapture(filePath)
    totalFrame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frameStep = int(totalFrame / (frameCount + 1))
    FID = 0
    while (cap.isOpened() and FID < frameCount):
        FID += 1
        frameID = FID * frameStep
        print(frameID)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameID)
        ret, frame = cap.read()
        width, height, _ = frame.shape
        if width > height:
            scale = frameSize / width
        else:
            scale = frameSize / height
        frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frames.append(image)
    cap.release()
    return frames


def saveRaw2IMG(RawPath, IMGPath):
    path = RawPath
    with rawpy.imread(path) as raw:
        rgb = raw.postprocess()
    imageio.imsave(IMGPath, rgb)


def saveRaw2IMG16(RawPath, IMGPath):
    with rawpy.imread(RawPath) as raw:
        rgb = raw.postprocess(gamma=(18, 10), no_auto_bright=True, output_bps=16)
    imageio.imsave(IMGPath, rgb)


def saveVideoFrameAsThumb(filePath):
    st = time.time()
    img = getVideoFrame(filePath, 0)
    tga = "C:\Temp\Thumbnails\%s.jpg" % uuid.uuid4()
    img = getResizedImg(img, 144)
    img.save(tga)
    et = time.time() - st
    print("Use %.3f sec to save %s: " % (et, tga))


def saveThumbnail(filePath, frameSize, thumbPath):
    # print("saveThumbnail :", filePath, frameSize, thumbPath)
    thumb = getThumbnail(filePath, frameSize)
    thumb.save(thumbPath)
    thumb.close()


def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        print(path + ' -- Folder Created Successfully')
        os.makedirs(path)
        return True
    else:
        print(path + ' -- Folder Already Exists')
        return False


def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        zf.write(tar, arcname)
    zf.close()


def findThumb(filePath, cachePath):
    MD5 = getDraftMD5(filePath)
    print("Draft MD5: ", MD5)
    errorPath = 'GUI/error.png'
    tga = os.path.join(cachePath, str(MD5) + ".jpg")
    if os.path.isfile(tga):
        return tga
    else:
        mkdir(cachePath)
        try:
            saveThumbnail(filePath, 144, tga)
        except:
            saveThumbnail(errorPath, 144, tga)
        return tga


################################################################
### 多线程加速 ###
def multiThread(mainList, function, threadCount):
    exitFlag = 0

    class myThread(threading.Thread):
        def __init__(self, threadID, name, q):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.q = q

        def run(self):
            print("开启线程：" + self.name)
            process_data(self.name, self.q)
            print("退出线程：" + self.name)

    def process_data(threadName, q):
        while not exitFlag:
            queueLock.acquire()
            if not workQueue.empty():
                data = q.get()
                queueLock.release()
                # PD.download(data)
                function(data)
            else:
                queueLock.release()

    threadList = []
    for i in range(0, threadCount):
        tempThreadName = 'thread-%d' % i
        print(tempThreadName)
        threadList.append(tempThreadName)
    queueLock = threading.Lock()
    workQueue = queue.Queue()
    threads = []
    threadID = 1

    # 创建新线程
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    # 填充队列
    queueLock.acquire()
    for item in mainList:
        workQueue.put(item)
    queueLock.release()

    # 等待队列清空
    while not workQueue.empty():
        pass

    # 通知线程是时候退出
    exitFlag = 1

    # 等待所有线程完成
    for t in threads:
        t.join()


################################################################
################################################################
### 多进程加速 ###
def multiProcess(mainList, function, threadCount):
    p = Pool(threadCount)
    for i in mainList:
        # print("MultiProcess Start :",i)
        p.apply_async(function, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()


################################################################

def fastSaveThumbnail(path):
    # tga = "temp\\Thumbnail\\%s.jpg" % uuid.uuid4()
    tga = "C:\Temp\Thumbnails\%s.jpg" % str(getMD5(path))
    saveThumbnail(path, 144, tga)


def main():
    path = r"D:\Python\AutoEditor\Images"
    # path = r"D:\Python\AutoEditor\Raw"
    # path = r"D:\DCIM\产品组团建170621"
    for i in os.listdir(path):
        file = os.path.join(path, i)
        tga = os.path.join(r"D:\Python\AutoEditor\temp\thumbnail", i.split(".")[0] + ".jpg")
        print("\n", file)
        getThumbnail(file, tga)
        print(getRawExif(file))


def main2():
    path = r"D:\Test Clips\IMA"
    files = getAllFiles(path)
    print("Get %d files" % len(files))
    images = []
    for file in files:
        kind = filetype.guess(file)
        if kind is None:
            pass
        else:
            if "image" in str(kind.mime):
                images.append(file)
                # thumbnails.append(getThumbnail(file,144))
                # st = time.time()
                # tga = r"temp\thumbnail\%s.jpg"%uuid.uuid4()
                # saveThumbnail(file,144,tga)
                # et = time.time() - st
                # print("Use time: ", et)
    # multiThread(images, fastSaveThumbnail, 200)
    multiProcess(images, fastSaveThumbnail, 56)
    # multiThread(images, fastSaveThumbnail, 160)


def main3():
    files = getAllFiles(r"D:\Test Clips\London")
    videos = []
    for file in files:
        kind = filetype.guess(file)
        if kind is not None:
            if "video" in str(kind.mime):
                videos.append(file)
    # multiProcess(videos, saveVideoFrameAsThumb, 12)
    multiThread(videos, saveVideoFrameAsThumb, 2)


def main4():
    path = r"temp\G3.MOV"
    frames = getVideoFrames(path, 320, 25)
    for frame in frames:
        tga = r"temp\\frames\\%.2f.png" % time.time()
        frame.save(tga)
    print(len(frames))
    pass


def main5():
    path = r"D:\Test Clips\London"
    files = getAllFiles(path)
    videos = []
    for file in files:
        kind = filetype.guess(file)
        if kind is not None:
            if "video" in str(kind.mime):
                videos.append(file)
    print("Videos :", len(videos))
    multiThread(videos, getMediaInfo, 23)
    # multiProcess(videos, getMediaInfo, 7)


def main6():
    # path = r"D:\Test Clips\IMA"
    path = r"D:\Test Clips"
    files = getAllFiles(path)
    # videos = []
    # for file in files:
    #     kind = filetype.guess(file)
    #     if kind is None:
    #         pass
    #     else:
    #         if "video" in str(kind.mime):
    #             videos.append(file)
    # # multiThread(images, getMD5, 4)
    # multiProcess(files, getMD5, 4)
    multiProcess(files, getDraftMD5, 1)


if __name__ == '__main__':
    st = time.time()

    main6()

    et = time.time() - st
    print("All Use time: ", et)
