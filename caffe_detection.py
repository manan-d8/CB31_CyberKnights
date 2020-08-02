import os,glob
import cv2 as cv
import numpy as np
import os.path
import os
from pyimagesearch.utils import Conf
import imutils
from tqdm import tqdm
path = r"<Directory path>/*.jpg"
lis = glob.glob(path)
no=0
import csv        

confThreshold = 0.5  
nmsThreshold = 0.4  
inpWidth = 416 
inpHeight = 416
classes = None
counter = 0
CLASSES = ["background","car","bus","motorbike"]

conf = Conf("config.json")
net = cv.dnn.readNetFromCaffe(conf["prototxt_path"],conf["model_path"])

net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

#config file in same directory or mention path
conf = Conf("config.json")
def detection_tsv(data,w_or_a):
    with open('CyberKnights_DETECTION.tsv', w_or_a, newline='') as f_output:
        tsv_output = csv.writer(f_output, delimiter='\t')
        tsv_output.writerow(data)

no =0
data_ocr=["Image","OCR"]
detection_ocr=["Image","BBox","Label"]
detection_tsv(detection_ocr,"w")
pts=[]
classname=""
for l in tqdm(lis):
    classname=""
    pts=[]
    try:
        no+=1    
        img = cv.imread(l)
        img = imutils.resize(img, width=conf["frame_width"])

        counter+=1

        blob = cv.dnn.blobFromImage(img, size=(300, 300),ddepth=cv.CV_8U)
        net.setInput(blob, scalefactor=1.0/127.5, mean=[127.5,127.5, 127.5])
        detections = net.forward()

        H,W,_ = img.shape
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated
            # with the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence`
            # is greater than the minimum confidence
            if confidence > conf["confidence"]:
                # extract the index of the class label from the
                # detections list
                idx = int(detections[0, 0, i, 1])

                # if the class label is not a in detection classes, ignore it

                if CLASSES[idx] not in[ "background","car","motorbike","bus"]:
                    continue

                (H, W) = img.shape[:2]
                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = box.astype("int")
                H,W,_ = img.shape
                f=cv.rectangle(img, (startX, startY), (endX, endY), (255, 178, 50), 5)
                cv.putText(f, CLASSES[idx], (startX,startY), cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3,cv.LINE_AA)
                cv.putText(f, CLASSES[idx], (startX,startY), cv.FONT_HERSHEY_SIMPLEX,1,(0,0,0),3,cv.LINE_AA)
                cv.putText(f, CLASSES[idx], (startX,startY), cv.FONT_HERSHEY_SIMPLEX,1,(0,255,255),1,cv.LINE_AA)
                # fPathTxt = l[36:-4]
                pts=[startX,startY,endX,endY]
                classname=CLASSES[idx]
                base=os.path.basename(l)
                
            # cv.imshow("frame" , img)
            # cv.waitKey(0)
            cv.imwrite("<saving directory path>"+str(no)+".jpg",img)
            
    except Exception as e:
        pass
