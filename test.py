Raw = []
new = []
for i in range(10):
    Raw.append(i)


print(Raw)
sample = 3
step = len(Raw)/sample
for i in range(3):

    inpoint = int(i*step)
    outpoint = int((i+1)*step)
    print("IN:%d OUT:%d"%(inpoint,outpoint))
    tempSeg = Raw[inpoint:outpoint]
    # tempSeg.append(Raw[inpoint:outpoint])
    new.append(max(tempSeg))
    print(tempSeg)

print(new)