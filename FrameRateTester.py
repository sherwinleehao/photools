import cv2
import numpy as np
import time

# events = [i for i in dir(cv2) if 'EVENT' in i]
# print (events)

# def mosueEventOnCV(event, x, y, flags, param):
#     if event == cv2.EVENT_MOUSEMOVE:
#         print('EVENT_MOUSEMOVE')
#         cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)
#
#
# cv2.namedWindow('capture')
# cv2.setMouseCallback('capture', mosueEventOnCV)
#
# cap = cv2.VideoCapture(0)
# while(1):
#     # get a frame
#     ret, frame = cap.read()
#     # show a frame
#     cv2.imshow("capture", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()

global img,crop,oldImg,oldTime
global point1, point2
global FPSList

oldTime = time.time()

FPSList = []
for i in range(300):
    FPSList.append(12)


def updateFPSList(deltaTime):

    global FPSList
    FPSList = FPSList[1:]
    FPSList.append(1/deltaTime)
    print("updateFPSList", FPSList[-1])

def on_mouse(event, x, y, flags, param):
    global img, point1, point2
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:         #左键点击
        point1 = (x,y)
        print("EVENT_LBUTTONDOWN",point1)
        cv2.circle(img2, point1, 10, (0,255,0), 2)
        cv2.imshow('get ROI', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):               #按住左键拖曳
        cv2.rectangle(img2, point1, (x,y), (255,0,0), 2)
        cv2.imshow('get ROI', img2)
    elif event == cv2.EVENT_LBUTTONUP:         #左键释放
        global crop
        point2 = (x,y)
        print("EVENT_LBUTTONUP", point2)
        cv2.rectangle(img2, point1, point2, (0,0,255), 2)
        cv2.imshow('get ROI', img2)
        # min_x = min(point1[0],point2[0])
        # min_y = min(point1[1],point2[1])
        # width = abs(point1[0] - point2[0])
        # height = abs(point1[1] -point2[1])
        # crop = img[min_y:min_y+height, min_x:min_x+width]
        showROI()
        # print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxx ',point1, point2)


def getROI():
    global img
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    cv2.namedWindow('get ROI')
    cv2.setMouseCallback('get ROI', on_mouse)
    cv2.imshow("get ROI", img)
    cap.release()
    cv2.waitKey(0)

def showROI():
    global point1, point2
    cap = cv2.VideoCapture(0)
    while(1):
        ret, frame = cap.read()
        min_x = min(point1[0],point2[0])
        min_y = min(point1[1],point2[1])
        width = abs(point1[0] - point2[0])
        height = abs(point1[1] -point2[1])
        crop = frame[min_y:min_y+height, min_x:min_x+width]
        isUpdated(crop)
        state = updateFPSState()


        cv2.imshow("crop", crop)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow("state", state)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def isUpdated(newImg):
    isupdate = False
    deltaValue = 0
    deltaTime = 0
    global oldImg
    global oldTime
    nImg = cv2.resize(newImg, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_NEAREST)
    try:
        matte = nImg - oldImg
        matte_gray = cv2.cvtColor(matte, cv2.COLOR_BGR2GRAY)
        deltaValue = sum(sum(matte_gray))
        print("detalValue :",deltaValue)
    except:
        pass

    oldImg = nImg
    if deltaValue >100:
        isupdate = True
        deltaTime = time.time()-oldTime
        oldTime = time.time()
        updateFPSList(deltaTime)

    return isupdate,deltaTime

def updateFPSState():

    global FPSList
    # print("updateFPSState",FPSList)
    height = 60
    width = len(FPSList)
    state = np.zeros((height,width, 3), np.uint8)
    for i in range(len(FPSList)):
        if FPSList[i] >= 27:
            lineColor = (0, 255, 0)
        elif FPSList[i] >= 21:
            lineColor = (0, 220,220)
        else :
            lineColor = (0, 0, 255)

        cv2.line(state, (i, height), (i, int(height-FPSList[i])), lineColor, 1)
    return state


def main():
    getROI()
    showROI()

if __name__ == '__main__':
    main()