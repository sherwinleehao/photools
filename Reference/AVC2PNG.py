import ffmpy
import subprocess
import json
import time


def saveThumbnails(input, output, count):
    meta = getMdeiaInof(input)
    duration = float(meta['streams'][0]['duration'])
    frameRate = int(meta['streams'][0]['r_frame_rate'].split("/")[0])/int(meta['streams'][0]['r_frame_rate'].split("/")[1])
    _,ts = getTimestamp(duration,frameRate)
    r = count/duration
    print(duration)
    print(frameRate)
    print(duration*frameRate)
    # ff = ffmpy.FFmpeg(inputs={input: None}, outputs={output + '_%10d.png': '-r 60 -ss 00:00:10 -t 00:00:01'})

    ff = ffmpy.FFmpeg(inputs={input: None}, outputs={output + '_%4d.png': '-s:v 640*360 -r %f -ss 00:00:00 -t %s'%(r,ts)})
    print(ff.cmd)
    ff.run()


def getMdeiaInof(path):
    tup_resp = ffmpy.FFprobe(
        inputs={path: None},
        global_options=['-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams']).run(
        stdout=subprocess.PIPE)
    meta = json.loads(tup_resp[0].decode('utf-8'))
    return meta

def getTimestamp(duration,frameRate):
    if duration >=86400:
        duration = 86399
    intTime = int(duration)
    decimal = duration-intTime
    hh = intTime // 3600
    mm = (intTime-hh*3600) // 60
    ss = intTime % 60
    ff = int(round(decimal*frameRate))
    dd = round(decimal*1000)
    time0 = "%02d:%02d:%02d.%02d" % (hh,mm,ss,ff)
    time1 = "%02d:%02d:%02d.%03d" % (hh,mm,ss,dd)

    return time0,time1

if __name__ == '__main__':
    st = time.time()
    inputPath = r'/Users/ws/Documents/Temp/04.mp4'
    inputPath = r'/Users/ws/Documents/Temp/Sync_Test_60FPS.mp4'
    outputPaht = r'/Users/ws/Documents/Temp/Thumbnails/xxxxxxx'
    saveThumbnails(inputPath, outputPaht, 250)

    et = time.time()
    print("used time:", et - st)
