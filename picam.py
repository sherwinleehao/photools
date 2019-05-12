import cv2
import numpy as np
import time

global img
global sample_img
# global point1, point2
global target
global target_w
global target_h
global search_w
global search_h
global template
global LMB
global match_val
global targets
global target_scale
global threshold
global roi

def init():
    global target,target_w,target_h,search_h,search_w,template
    global LMB
    global match_val
    global targets
    global target_scale
    global threshold
    targets = []
    match_val = 0
    LMB = 0
    target = (0,0)
    target_w = 20
    target_h = 20
    search_w = 80
    search_h = 80
    target_scale = 8
    threshold = 0.8
    template = np.zeros((target_h, target_h, 3), np.uint8)
    targets.append(target)

def clamp(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n

def update_template():
    global img
    global target, target_w, target_h, template
    h, w, _ = img.shape
    x = target[0]
    y = target[1]
    xl = x - int(target_w / 2)
    xr = x + int(target_w / 2)
    yu = y - int(target_h / 2)
    yd = y + int(target_h / 2)

    xl = clamp(xl, 0, w - 1)
    xr = clamp(xr, 1, w)
    yu = clamp(yu, 0, h - 1)
    yd = clamp(yd, 1, h)
    template = img[yu:yd, xl:xr]
    print("Update Template.")

def draw_target(point,img):
    global target_w, target_h, search_h, search_w
    global match_val
    global threshold
    global roi
    h, w, _ = img.shape
    x = point[0]
    y = point[1]
    xl = x - int(target_w/2)
    xr = x + int(target_w/2)
    yu = y - int(target_h/2)
    yd = y + int(target_h/2)

    xl = clamp(xl, 0, w-1)
    xr = clamp(xr, 1, w)
    yu = clamp(yu, 0, h-1)
    yd = clamp(yd, 1, h)

    tga_rectColor = (0,0,0)
    sch_rectColor = (0,0,0)
    if match_val >threshold:
        tga_rectColor = (255,255,255)
        sch_rectColor = (0,255,0)
    else:
        tga_rectColor = (0,0,255)
        sch_rectColor = (0,0,255)


    roi = img[yu:yd, xl:xr].copy()
    # roi = cv2.resize(roi, None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST)
    cv2.rectangle(img, (x - int(target_w/2), y - int(target_h/2)), (x + int(target_w/2), y + int(target_h/2)), tga_rectColor, 1)
    cv2.rectangle(img, (x - int(search_w/2), y - int(search_h/2)), (x + int(search_w/2), y + int(search_h/2)), sch_rectColor, 1)

    # roi_h, roi_w, _ = roi.shape
    # img[(h-roi_h):h, 0:roi_w] = roi

    return img

def on_mouse(event, x, y, flags, param):
    global img, point1, point2 , sample_img
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:         #左键点击
        point1 = (x,y)
        cv2.circle(img2, point1, 10, (0,255,0), 2)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):               #按住左键拖曳
        cv2.rectangle(img2, point1, (x,y), (255,0,0), 2)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP:         #左键释放
        point2 = (x,y)
        cv2.rectangle(img2, point1, point2, (0,0,255), 2)
        cv2.imshow('image', img2)
        min_x = min(point1[0],point2[0])
        min_y = min(point1[1],point2[1])
        width = abs(point1[0] - point2[0])
        height = abs(point1[1] -point2[1])
        sample_img = img[min_y:min_y+height, min_x:min_x+width]
        # cv2.imwrite('sample.png', cut_img)

def on_mouse2(event, x, y, flags, param):
    global img,target
    global LMB
    if event == cv2.EVENT_LBUTTONDOWN:         #左键点击
        LMB = 1
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):         #左键点击
        LMB = 1
        target = (x,y)
        img = draw_target(target,img)
        cv2.imshow('image', img)
    elif event == cv2.EVENT_LBUTTONUP:
        LMB = 0
        target = (x, y)
        update_template()


def track():
    global img,template,LMB
    global target,search_w,search_h,target_w,target_h
    global match_val

    if target[0] and target[0] and LMB == 0:
        st = time.time()

        h, w, _ = img.shape
        x = target[0]
        y = target[1]

        sxl = x - int(search_w / 2)
        sxr = x + int(search_w / 2)
        syu = y - int(search_h / 2)
        syd = y + int(search_h / 2)

        sxl = clamp(sxl, 0, w - 1)
        sxr = clamp(sxr, 1, w)
        syu = clamp(syu, 0, h - 1)
        syd = clamp(syd, 1, h)

        search = img[syu:syd, sxl:sxr]

        match_score = cv2.matchTemplate(search, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(match_score)
        # rectColor = (0,0,0)
        # if max_val >0.8:
        #     rectColor = (0,255,0)
        # elif max_val >0.7:
        #     rectColor = (0,255,255)
        # elif max_val >0.5:
        #     rectColor = (0,0,255)
        # cv2.rectangle(img, max_loc, (max_loc[0]+temp_w, max_loc[1]+temp_h), rectColor, 2)
        # print(max_val)
        match_val = max_val

        offset = ((max_loc[0]-int(0.5*(search_w-target_w))),(max_loc[1]-int(0.5*(search_h-target_h))))
        target = (target[0]+offset[0],target[1]+offset[1])
        et =time.time()
        print("Used %.4f to track."%(et-st)," Offset:",offset," match_val:",match_val)

    else:
        return


def main():
    global img
    global target
    global target_w, target_h
    global target_scale
    global template
    global roi

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 360)
    while(cap.isOpened()):
            st = time.time()
            ret , img = cap.read()
            # img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
            track()

            img = draw_target(target, img)
            cv2.namedWindow('image')

            h,w,_ = img.shape
            canvas = np.zeros((h + target_scale*target_h, w, 3), np.uint8)
            canvas[0:h, 0:w] = img
            temp_template = cv2.resize(template,None,fx=target_scale,fy=target_scale,interpolation=cv2.INTER_NEAREST)
            canvas[h:(h + target_scale*target_h), 0:(target_scale*target_w)] = temp_template

            temp_roi = cv2.resize(roi,None,fx=target_scale,fy=target_scale,interpolation=cv2.INTER_NEAREST)
            temp_roi_h,temp_roi_w,_ = temp_roi.shape
            canvas[h:(h + temp_roi_h), (target_scale*target_w):(target_scale*target_w+temp_roi_w)] = temp_roi
            cv2.imshow("image", canvas)

            cv2.setMouseCallback('image', on_mouse2)
            cv2.waitKey(1)
            et = time.time()
            print("Update %.4f"%(et - st))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == '__main__':
    init()
    main()
