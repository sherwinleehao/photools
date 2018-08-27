import time
from pydub import AudioSegment
# sound = AudioSegment.from_file("D:/python/photools/Footages/test.mp3", format="mp3")
sound = AudioSegment.from_file("/Users/ws/Python/photools/Footages/test.mp3", format="mp3")
peak_amplitude = sound.max
loudness = sound.dBFS
print(loudness)

st = time.time()

wave = []

# for i in range(0,1024):
#     segment = sound[i*1000/4:(i+1)*1000/4]
#     wave.append(segment.max)

for i in range(0,10240):
    segment = sound[i*1000/40:(i+1)*1000/40]
    wave.append(segment.max)


et = time.time()

print("used time:",et-st)

print(wave)