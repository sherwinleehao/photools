import os
import shutil
import photools as pt


def getSlowMotion(path,tga):
    files = pt.getAllFiles(path)
    for file in files:
        if "Slo-Mo" in file:
            if "Original" not in file:
                shutil.move(file,tga)


def delRawFileWithoutJpg(path,tga):
    #查找path路径下有JPG而没有Raw文件的情况，然后删除对应的Raw文件
    files = pt.getAllFiles(path)
    jpgs = []
    raws = []
    for file in files:
        if ".JPG" in file:
            jpgs.append(file)
        elif '.ARW' in file:
            raws.append(file)

    for raw in raws:
        name = raw.replace('.ARW',".JPG")
        if name not in jpgs:
            print(name)
            shutil.move(raw, tga)
    # print(jpgs)
    # print(raws)


if __name__ == '__main__':
    # path = "F:/DCIM/2018-10-01/R1"
    path = "F:/DCIM/2018-10-01/DCIM/100MSDCF"
    tga = "F:/DCIM/2018-10-01/temp"
    delRawFileWithoutJpg(path,tga)
    # getSlowMotion(path,tga)