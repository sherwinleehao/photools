import time
from pydub import AudioSegment
sound = AudioSegment.from_file("Footages/test.mp3", format="mp3")
peak_amplitude = sound.max
loudness = sound.dBFS
print(loudness)

st = time.time()

for i in range(0,250):

    # second = i*1000

    segment = sound[i*1000:(i+1)*1000]
    print('%5d'%i,segment.max)

et = time.time()

print("used time:",et-st)
