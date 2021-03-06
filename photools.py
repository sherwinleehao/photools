#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Image Tool Library

Author: Sherwin Lee

Website: Sherwinleehao.com

Last edited: 20181226
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
from pydub import AudioSegment
import xmltodict
import re
import numpy as np

######## fill holes for AEC ########


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
    return int(color[0]), int(color[1]), int(color[2]), int(color[3])


def getSolidColor(b, g, r, h, w, d):
    img = np.zeros([h, w, d], np.uint8)
    img[:, :, 0] = np.ones([h, w]) * b
    img[:, :, 1] = np.ones([h, w]) * g
    img[:, :, 2] = np.ones([h, w]) * r
    return img


def getAlphaBlend(ima, imb, premult):
    if ima.shape == imb.shape:
        _, _, _, a = cv2.split(ima)
        a = a.astype(np.float) / 255
        h, w, d = ima.shape
        if d == 3:
            alpha = cv2.merge([a, a, a])
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


def initTga(path):
    mkdir(path)
    files = getAllFiles(path)
    for file in files:
        os.remove(file)


def saveAlphaInGreen(im, path):
    b, g, r, a = cv2.split(im)
    b[:][:] = 0
    dst = cv2.merge([b, a, b])
    cv2.imwrite(path, dst)


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


def code2text(code):
    hexmap = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "A": 10, "B": 11, "C": 12,
              "D": 13, "E": 14, "F": 15, }
    texts = []
    for i in range(int(len(code) / 4)):
        k = code[4 * i:4 * (i + 1)]
        x = hexmap[k[3]] + hexmap[k[2]] * 16 + hexmap[k[1]] * 16 * 16 + hexmap[k[0]] * 16 * 16 * 16
        texts.append(x)
    return texts


def intARGB2ARGB(val):
    color = str(hex((val + (1 << 32)) % (1 << 32))).replace("0x", "")
    A = int(color[0] + color[1], 16)
    R = int(color[2] + color[3], 16)
    G = int(color[4] + color[5], 16)
    B = int(color[6] + color[7], 16)

    return A, B, G, R


def intARGB2intRGB(val):
    color = str(hex((val + (1 << 32)) % (1 << 32))).replace("0x", "")
    if len(color) == 8:
        hexColor = color[6] + color[7] + color[4] + color[5] + color[2] + color[3]
    if len(color) == 6:
        hexColor = color[4] + color[5] + color[2] + color[3] + color[0] + color[1]
    return int(hexColor, 16)


def int2RGB(val):
    print('Color Index:',val)
    if val == 0:
        return 0.0,0.0,0.0

    color = str(hex(val)).replace('0x', '')
    R = int(color[0:2], 16)
    G = int(color[2:4], 16)
    B = int(color[4:6], 16)

    f_R = R / 255
    f_G = G / 255
    f_B = B / 255

    return f_R, f_G, f_B


def textcode2token(textcodeList, GUID):
    token = []
    header = {'@V': '1', '@Tp': '1', '@Jf': '1', '@Li': '0', '@Ri': '0', '@Fi': '0', '@Sb': '0', '@Sa': '0'}
    token.append(header)
    for textcode in textcodeList:
        Tk = {'@V': '1', '@Tp': '0', '@Ch': str(textcode), '@Ft': GUID}
        token.append(Tk)
    return token


####################################

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


def getAllImgs(path):
    files = getAllFiles(path)
    IMGs = []
    for file in files:
        if getFileKind(file) == "image":
            IMGs.append(file)
    return IMGs


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


def getImgSize(filePath):
    width = 0
    height = 0
    try:
        im = Image.open(filePath)
        width, height = im.size
    except:
        pass
    return width, height


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


def getWaveform(filePath, width, height):
    sound = AudioSegment.from_file(filePath, format="mp3")
    # step = len(sound) / width
    # wave = []
    # for i in range(0, width):
    #     segment = sound[i * step:(i + 1) * step]
    #     wave.append(segment.max)

    sample = 4
    step = len(sound) / (width * sample)
    rawwave = []
    wave = []

    for i in range(0, (width * sample)):
        segment = sound[i * step:(i + 1) * step]
        rawwave.append(segment.max)

    for i in range(0, width):
        segment = rawwave[i * sample:(i + 1) * sample]
        wave.append(sum(segment) / sample)

    waveform = Image.new('RGB', (width, height), (21, 96, 67))
    draw = ImageDraw.Draw(waveform)
    for i in range(len(wave)):
        value = height * (wave[i] / 32768)
        sp = (height - value) / 2
        draw.line((i, sp, i, value + sp), fill=(37, 208, 141))
    del draw
    return waveform


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
    img = getVideoFrame(filePath, 144, 8)
    tga = "/Users/ws/Desktop/comparation/Thumbnails/%s.jpg" % uuid.uuid4()
    img = getResizedImg(img, 144)
    img.save(tga)
    et = time.time() - st
    print("Use %.3f sec to save %s: " % (et, tga))


def saveThumbnail(filePath, frameSize, thumbPath):
    # print("saveThumbnail :", filePath, frameSize, thumbPath)
    thumb = getThumbnail(filePath, frameSize)
    thumb.save(thumbPath)
    thumb.close()


def saveWaveform(filePath, tgaPath, width, height):
    waveform = getWaveform(filePath, width, height)
    waveform.save(tgaPath)
    waveform.close()


def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        # print(path + ' -- Folder Created Successfully')
        os.makedirs(path)
        return True
    else:
        # print(path + ' -- Folder Already Exists')
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


def getFileKind(filePath):
    videoKind = ['mp4', 'mov', 'avi', 'webm', 'mts', 'wmv', 'mpg', '3gp', 'flv', 'mkv', 'vob', 'ts', 'wma', 'm4v',
                 'ogg', 'mpeg', 'mxf']
    imageKind = ['jpg', 'png', 'gif', 'cr2', 'arw']
    audioKind = ['mp3', 'wav', 'm4a']
    extension = os.path.splitext(filePath)[-1][1:].lower()
    if extension in videoKind:
        return "video"
    elif extension in imageKind:
        return "image"
    elif extension in audioKind:
        return "audio"
    else:
        return None


def getTimestamp(duration, frameRate):
    if duration >= 86400:
        duration = 86399
    intTime = int(duration)
    decimal = duration - intTime
    hh = intTime // 3600
    mm = (intTime - hh * 3600) // 60
    ss = intTime % 60
    ff = int(round(decimal * frameRate))
    dd = round(decimal * 1000)
    time0 = "%02d:%02d:%02d.%02d" % (hh, mm, ss, ff)
    time1 = "%02d:%02d:%02d.%03d" % (hh, mm, ss, dd)

    return time0, time1


def getKeyMediaInfo(mediaInfo):
    # if mediaInfo is None:
    #     return 0,0,0,0
    # else:
    streams = mediaInfo['streams']
    for stream in streams:
        if stream['codec_type'] == "video":
            height = stream['coded_height']
            width = stream['coded_width']
            fps = int(stream['avg_frame_rate'].split('/')[0]) / int(stream['avg_frame_rate'].split('/')[1])
            duration, _ = getTimestamp(float(stream['duration']), fps)
            return width, height, fps, duration


def findThumb(filePath, cachePath):
    MD5 = getDraftMD5(filePath)
    errorPath = 'GUI/error.png'
    tga = os.path.join(cachePath, str(MD5) + ".jpg")
    if os.path.isfile(tga):
        return tga
    else:
        mkdir(cachePath)
        kind = getFileKind(filePath)
        if kind is not None:
            print(filePath, "is ", kind)
            if "video" in kind:
                thumb = getVideoFrame(filePath, 144, 0)
                thumb.save(tga)
                thumb.close()
                return tga
                pass
            elif "image" in kind:
                saveThumbnail(filePath, 144, tga)
                return tga
            else:
                saveThumbnail(errorPath, 144, tga)
                return tga


def findWaveform(filePath):
    MD5 = getDraftMD5(filePath)
    print(filePath, " \nMD5 is :", MD5)
    tgaPath = os.path.join(r'Temp/Cache/%s.png' % str(MD5))
    # saveWaveform(filePath, tgaPath, 512, 128)
    if os.path.exists(tgaPath):
        return tgaPath
    else:
        saveWaveform(filePath, tgaPath, 512, 128)
        return tgaPath



def xml2dict(xmlstr):
    xmlparse = xmltodict.parse(xmlstr)
    jsonData = json.dumps(xmlparse)
    dictData = json.loads(jsonData)
    return dictData


def dict2xml(dict):
    xml = xmltodict.unparse(dict, pretty=True)
    regex = re.compile(r"></(.*?)>", re.IGNORECASE)
    final = regex.sub('/>', xml)
    return final


# def findMediaInfo(filePath, cachePath):
#     MD5 = getDraftMD5(filePath)
#     tga = os.path.join(cachePath, str(MD5) + ".json")
#     if os.path.isfile(tga):
#         mediaInfo = json.loads(open(tga,'r').read())
#         print(mediaInfo)
#         print(getKeyMediaInfo(mediaInfo))
#         return getKeyMediaInfo(mediaInfo)
#     else:
#         mkdir(cachePath)
#         kind = getFileKind(filePath)
#         if kind is "video":
#             mediaInfo = getMediaInfo(filePath)
#             mediaInfoJson = json.dumps(mediaInfo, sort_keys=True, indent=4, separators=(',', ': '))
#             f = open(tga, 'w')
#             f.write(mediaInfoJson)
#             f.close()
#             # mediaInfo[]
#             return getKeyMediaInfo(mediaInfo)
#         elif kind is "image":
#             mediaInfo = getMediaInfo(filePath)

def findMediaInfo(filePath, cachePath):
    MD5 = getDraftMD5(filePath)
    tga = os.path.join(cachePath, str(MD5) + ".json")
    mkdir(cachePath)
    kind = getFileKind(filePath)
    if kind is "video":
        if os.path.isfile(tga):
            mediaInfo = json.loads(open(tga, 'r').read())
            print(getKeyMediaInfo(mediaInfo))
            return getKeyMediaInfo(mediaInfo)
        else:
            mediaInfo = getMediaInfo(filePath)
            mediaInfoJson = json.dumps(mediaInfo, sort_keys=True, indent=4, separators=(',', ': '))
            f = open(tga, 'w')
            f.write(mediaInfoJson)
            f.close()
            # mediaInfo[]
            return getKeyMediaInfo(mediaInfo)
    elif kind is "image":
        if os.path.isfile(tga):
            mediaInfo = json.loads(open(tga, 'r').read())
            width = mediaInfo['width']
            height = mediaInfo['height']
            return width, height, 0.0, "——"
        else:
            width, height = getImgSize(filePath)
            mediaInfo = {'width': width, 'height': height}
            mediaInfoJson = json.dumps(mediaInfo, sort_keys=True, indent=4, separators=(',', ': '))
            f = open(tga, 'w')
            f.write(mediaInfoJson)
            f.close()
            return width, height, 0.0, "——"


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
    # files = getAllFiles(r"D:\Test Clips\London")
    # files = getAllFiles(r"C:\Footages\import_test")
    files = getAllFiles(r"/Users/ws/Desktop/comparation/import_test")
    # files = getAllFiles(r"D:\comparation\import_test")
    videos = []
    for file in files:
        kind = getFileKind(file)
        if kind is "video":
            videos.append(file)
    # multiProcess(videos, saveVideoFrameAsThumb, 2)
    multiThread(videos, saveVideoFrameAsThumb, 4)


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

    # main3()
    findWaveform(r'D:/CloudMusic/C AllStar - 天光.mp3')
    et = time.time() - st
    print("All Use time: ", et)
