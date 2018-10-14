from PIL import ImageGrab
import numpy
import cv2

# im = ImageGrab.grab()
im = ImageGrab.grab(bbox=(0, 0, 3840, 2160))
im.save('Temp/Test.png','png')
# img = cv2.cvtColor(numpy.asarray(im),cv2.COLOR_RGB2BGR)
# cv2.imshow("OpenCV",img)
# cv2.waitKey(0)