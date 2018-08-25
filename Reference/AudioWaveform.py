import time
from pydub import AudioSegment
# sound = AudioSegment.from_file("D:/python/photools/Footages/test.mp3", format="mp3")
sound = AudioSegment.from_file("/Users/ws/Python/photools/Footages/test.mp3", format="mp3")
peak_amplitude = sound.max
loudness = sound.dBFS
print(loudness)

st = time.time()

wave = []
for i in range(0,1024):

    # second = i*1000

    segment = sound[i*1000/4:(i+1)*1000/4]
    print('%5d'%i,segment.max)
    # wave.append([i,segment.max])
    wave.append(segment.max)
et = time.time()

print("used time:",et-st)

print(wave)