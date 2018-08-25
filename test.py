import math

a = []
for i in range(0,100):
    a.append(i/100)

print(a)

for i in a:
    v = math.pow(i,0.5)
    print(i,v)