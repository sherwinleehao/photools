import os,time
import filetype
from multiprocessing import Pool

def multiProcess(mainList, function, threadCount):
    p = Pool(threadCount)
    for i in mainList:
        # print("MultiProcess Start :",i)
        p.apply_async(function, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()


def isVideo(path):
    ftype = path.split(".")[-1].lower()
    if "mp4" in ftype or "mov" in ftype :
        return True
    else:
        kind = filetype.guess(path)
        if kind is None:
            # print(path,"is not a Video")
            return False
        else:
            if "video" in kind.mime:
                return True

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def get_cmd():
    CMDs = []
    scale = r"-s:v 640*360"
    path = os.getcwd()
    for i in os.listdir(path):
        # print(i)
        file = os.path.join(path, i)
        # print(file)
        if os.path.isfile(file):
            if isVideo(file):
                formatName = file.split(".")[-1]
                formatName = r"." + formatName
                ttga = file.replace(formatName, ".MP4")
                fileName = os.path.basename(ttga)
                tga = ttga.replace(fileName, "VGA\\" + fileName)
                folder = ttga.replace(fileName, "VGA")
                mkdir(folder)
                # print(folder)
                # cmd = '''ffmpeg -i "%s"  -c:v libx265 -b:v 1000K %s "%s"  -y''' % (file, scale, tga)
                cmd = '''ffmpeg -i "%s"  -c:v hevc_nvenc -b:v 1000K %s "%s"  -y''' % (file, scale, tga)
                print(cmd)
                CMDs.append(cmd)
                # os.system(cmd)
    return CMDs

def run_cmd(cmd):
    os.system(cmd)

if __name__ == '__main__':
    cmds = get_cmd()
    multiProcess(cmds,run_cmd,1)


