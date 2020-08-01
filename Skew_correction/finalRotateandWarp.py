import cv2
import numpy as np
from scipy.spatial import distance as dist
from imutils import paths
from scipy.ndimage import interpolation as inter
import statistics
import glob
import time

def area_avg(ctrs):
    area=[]
    for i, ctr in enumerate(ctrs):
        rect = cv2.minAreaRect(ctr)
        rbox = order_points(cv2.boxPoints(rect))
        w = np.linalg.norm([rbox[0, 0] - rbox[1, 0], rbox[0, 1] - rbox[1, 1]])
        h = np.linalg.norm([rbox[0, 0] - rbox[-1, 0], rbox[0, 1] - rbox[-1, 1]])
        ar = float(w)/h
        if ar>1.2 and (w*h)>15000:
            area.append(w*h)
    if(len(area)>0):
        
        avg = statistics.mean(area)
    else:
        avg=0
    # print("avg",avg)
    return(avg)

def correct_skew(image, delta=1, limit=50):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
        return histogram, score

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
              borderMode=cv2.BORDER_REPLICATE)

    return best_angle, rotated

def order_points(pts):
        xSorted = pts[np.argsort(pts[:, 0]), :]
        leftMost = xSorted[:2, :]
        rightMost = xSorted[2:, :]
        leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
        (tl, bl) = leftMost
        D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
        (br, tr) = rightMost[np.argsort(D)[::-1], :]
        return np.asarray([tl, tr, br, bl], dtype=pts.dtype)



def crop_and_warp(img, rect):
    rbox = order_points(cv2.boxPoints(rect))
    width = np.linalg.norm([rbox[0, 0] - rbox[1, 0], rbox[0, 1] - rbox[1, 1]])
    height = np.linalg.norm([rbox[0, 0] - rbox[-1, 0], rbox[0, 1] - rbox[-1, 1]])
    src = rbox.astype(np.float32)
    dst = np.array([[0, 0],
                            [width - 1, 0],
                             [width - 1, height - 1],
                             [0, height - 1]], dtype="float32")
    m = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(img, m, (width, height)) 

def get_bounding_box(count,image):
    # cv2.imshow('image_YUV',image)
    # cv2.waitKey(0)
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blurred = cv2.GaussianBlur(imgray,(5,5),0)
    thresh = cv2.adaptiveThreshold(image_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 3)
    edges = cv2.Canny(thresh,10,400)
    contours,hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    avgContours=area_avg(contours)
    m = max(contours, key = cv2.contourArea)
    x,y,w,h = cv2.boundingRect(m)
    maxArea=w*h
    if(avgContours==0 or maxArea<10000):
        # print("once")
        equ = cv2.equalizeHist(imgray)
        image_blurred = cv2.GaussianBlur(equ,(7,7),0)
        thresh = cv2.adaptiveThreshold(image_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 3)
        edges = cv2.Canny(thresh,10,400)
        contours,hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    avgContours=area_avg(contours)
    m = max(contours, key = cv2.contourArea)
    x,y,w,h = cv2.boundingRect(m)
    maxArea=w*h
    if(avgContours==0 or maxArea<10000):
        # print("twice")
        th, bw = cv2.threshold(imgray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        edges = cv2.Canny(imgray, th/2, th)
        contours,hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        
    m = max(contours, key = cv2.contourArea)
    x,y,w,h = cv2.boundingRect(m)
    maxArea=w*h
    # print(maxArea)
    if(avgContours>maxArea):
        maxArea=avgContours
    bestCs=[]
    areas=[]
    for i,c in enumerate(contours):
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        rbox = order_points(box)
        w = np.linalg.norm([rbox[0, 0] - rbox[1, 0], rbox[0, 1] - rbox[1, 1]])
        h = np.linalg.norm([rbox[0, 0] - rbox[-1, 0], rbox[0, 1] - rbox[-1, 1]])
        #aspect_ratio = float(w)/h
        area=w*h
        if(area<=maxArea and area>8000):
            imgC = crop_and_warp(image,rect)
            areas.append(w*h)
            bestCs.append(i)
            
    if(len(areas)==0):
        #imgC = crop_and_warp(image,rect)
        cv2.imwrite("Results/didntWarp"+str(count)+".jpg",image)
    else:
        bestMax=max(areas)
        index=areas.index(bestMax)
        idx=bestCs[index]
        rect=cv2.minAreaRect(contours[idx])
        imgC = crop_and_warp(image,rect)
        cv2.imwrite("Results/warped"+str(count)+".jpg",imgC)
        

if __name__ == '__main__':
    file_path = 'Testimgs/*.jpg'
    image_paths = glob.glob(file_path)
    count=1
    for image in image_paths:
        imgPlate=cv2.imread(image)
        imgRS = cv2.resize(imgPlate, (400, 150), fx = 1.87, fy = 1.97,interpolation=cv2.INTER_LINEAR)
        image = cv2.imread('rotated26.jpg')
        t1 = time.time()
        angle, rotated = correct_skew(imgRS)
        print(' [ Time  ] ',time.time()-t1)
        imgRT = cv2.resize(rotated, (400, 150), fx = 1.87, fy = 1.97,interpolation=cv2.INTER_LINEAR)
        # print(angle)
        cv2.imwrite("Results/Rotated"+str(count)+".jpg",imgRT)
        get_bounding_box(count,imgRT)
        count+=1