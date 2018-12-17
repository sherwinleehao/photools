import cv2
from PIL import Image, ImageDraw, ExifTags
import numpy as np

def getBeautyLayer(path):
    img = cv2.imread(path,-1)
    B, G, R, A = cv2.split(img);

    nB = (B/255)*(A/255)
    nG = (G/255)*(A/255)
    nR = (R/255)*(A/255)
    cv2.namedWindow("Image")
    print(nB[:][200])
    # cv2.imshow("Image", img)
    newImg = cv2.merge([nB, nG, nR])
    print("New Image dtype",newImg.dtype)
    img = np.array(newImg*255, dtype=np.uint8)
    # cv2.imwrite(r'Temp/Test_fill_hole2.png',newImg, dtype = "uint8")
    cv2.imwrite(r'Temp/Test_fill_hole2.png',img)
    cv2.imshow("Image", newImg)
    cv2.waitKey(0)

if __name__ == '__main__':
    path = r'Temp/Test_fill_hole.png'
    getBeautyLayer(path)