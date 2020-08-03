import os,glob
from shutil import copyfile
import cv2 as cv
import sys
import numpy as np
import os.path
import os
from pyimagesearch.utils import Conf
import imutils
import  time
from tqdm import tqdm
path = r"E:\0NewDev\SIH\DetectionDay2\*.jpg"
lis = glob.glob(path)
no=0
import xml.etree.cElementTree as ET
from PIL import Image
import csv        
import NoPlateDetector as NPD
import CyberKnightsOCRTsv as CKOT
import newSkew as skw
NpdObj = NPD.No_Plate_Detector()
CKOTOBJ = CKOT.Character_Detector()
ttt1 = time.time()
ANNOTATIONS_DIR_PREFIX = "annotation"

DESTINATION_DIR = "converted_labels"

confThreshold = 0.5  
nmsThreshold = 0.4  
inpWidth = 416 
inpHeight = 416
classes = None
counter = 0
CLASSES = ["background","car","motorbike","bus"]

conf = Conf("config.json")
net = cv.dnn.readNetFromCaffe(conf["prototxt_path"],conf["model_path"])

net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


conf = Conf("config.json")
def detection_tsv(data,w_or_a):
	with open('CyberKnights_DETECTION.tsv', w_or_a, newline='') as f_output:
		tsv_output = csv.writer(f_output, delimiter='\t')
		tsv_output.writerow(data)

	
def create_root(file_prefix, width, height):
	root = ET.Element("annotation")
	ET.SubElement(root, "filename").text = "{}.jpg".format(file_prefix)
	ET.SubElement(root, "folder").text = "images"
	size = ET.SubElement(root, "size")
	ET.SubElement(size, "width").text = str(width)
	ET.SubElement(size, "height").text = str(height)
	ET.SubElement(size, "depth").text = "3"
	return root


def create_object_annotation(root, voc_labels):
	for voc_label in voc_labels:
		obj = ET.SubElement(root, "object")
		ET.SubElement(obj, "name").text = voc_label[0]
		ET.SubElement(obj, "pose").text = "Unspecified"
		ET.SubElement(obj, "truncated").text = str(0)
		ET.SubElement(obj, "difficult").text = str(0)
		bbox = ET.SubElement(obj, "bndbox")
		ET.SubElement(bbox, "xmin").text = str(voc_label[1])
		ET.SubElement(bbox, "ymin").text = str(voc_label[2])
		ET.SubElement(bbox, "xmax").text = str(voc_label[3])
		ET.SubElement(bbox, "ymax").text = str(voc_label[4])
	return root

def create_file(file_prefix, width, height, voc_labels):
	root = create_root(file_prefix, width, height)
	root = create_object_annotation(root, voc_labels)
	tree = ET.ElementTree(root)
	tree.write("{}/{}.xml".format(r'E:\0NewDev\SIH\Day1', file_prefix))
no =0
data_ocr=["Image","OCR"]
detection_ocr=["Image","BBox","Label"]
detection_tsv(detection_ocr,"w")
pts=[]
classname=""


cap = cv.VideoCapture(r'E:\0NewDev\New\Data\test2.mp4')


# cap.set(cv.cv.CV_CAP_PROP_FPS, 20)
# Check if camera opened successfully
if (cap.isOpened()== False): 
	print("Error opening video stream or file")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
# out = cv.VideoWriter('Detection_vid1.mp4',cv.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
result = cv.VideoWriter('filename.avi',  cv.VideoWriter_fourcc(*'MJPG'), 10, (frame_width,frame_height)) 
    
no=0
while(True):
	no+=1
	ret, img = cap.read()
	classname=""
	pts=[]
	print('-'*60,no)
	try:
		no+=1    
		img2 = img.copy()
		img3 = img.copy()
		img = imutils.resize(img, width=conf["frame_width"])

		counter+=1

		blob = cv.dnn.blobFromImage(img, size=(300, 300),ddepth=cv.CV_8U)
		net.setInput(blob, scalefactor=1.0/127.5, mean=[127.5,127.5, 127.5])
		detections = net.forward()
		vocl = []

		H,W,_ = img.shape
		flag = True
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

				# if the class label is not a car, ignore it

				if CLASSES[idx] not in[ "background","car","motorbike","bus"]:
					continue

				(H, W) = img.shape[:2]
				box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
				(startX, startY, endX, endY) = box.astype("int")
				h,w,_   = img.shape
				H,W,_   = img2.shape
				print(H,W,h,w)
				if startX < 0:
					startX = 0
				if startY < 0 :
					startY = 0
				if endX > w:
					endX = w
				if endY > h:
					endY = h


				print(startX, startY, endX, endY)

				startXn = W*startX//w
				startYn = H*startY//h
				endXn   = W*endX//w
				endYn   = H*endY//h

				print(startXn, startYn, endXn, endYn)
				vehicleid = CLASSES[idx]
				img3 = cv.rectangle(img3, (startXn, startYn), (endXn, endYn), (255, 178, 50), 7)
				img3 = cv.rectangle(img3, (startXn, startYn), (endXn, endYn), (0, 0, 0), 3)
				cv.putText(img3 ,str(vehicleid),(startXn, startYn),cv.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 	3 , cv.LINE_AA)
				pts=[startXn,startYn,endXn,endYn]
				classname=CLASSES[idx]
				# base=os.path.basename()
				# det_data=[base,pts,classname]
				# detection_tsv(det_data,"a")
				tempimg = img2[startYn:endYn , startXn:endXn]
				Noplate_Ret = NpdObj.Check_if_NoPlate_Exist(tempimg)
				print('back')
				print(Noplate_Ret)
				if Noplate_Ret[0]:
					n=0
					flag = False
					for i,res in enumerate(Noplate_Ret[1]):
						try:
							cv.rectangle(img3, ( startXn+res[1],startYn+res[0]), (startXn+res[1]+res[2], startYn+res[0]+res[3]), (255, 178, 50), 7)
							cv.rectangle(img3, ( startXn+res[1],startYn+res[0]), (startXn+res[1]+res[2], startYn+res[0]+res[3]), (0, 0, 0), 3)
							skewObj=skw.newSkew()

							imgppp= img2[ startYn+res[0]:startYn+res[0]+res[3],startXn+res[1]:startXn+res[1]+res[2]]
							print('[skewimg up]',imgppp.shape)

							# cv.imshow('fffff',img3)
							# cv.waitKey(0)							
							# cv.imshow('fff',imgppp)
							# cv.waitKey(0)
							Noplate_Skew_img=skewObj.StartProcess(imgppp)
							t1 = time.time()
							ret = CKOTOBJ.Detect_Characters(Noplate_Skew_img)
							cv.putText(img3 ,str(ret),(startXn+res[1],startYn+res[0]),cv.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 3 , cv.LINE_AA)
							# cv.putText(img3 ,str(ret),(startXn+res[1],startYn+res[0]),cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 		2 , cv.LINE_AA)
							# cv.putText(img3 ,str(ret),(startXn+res[1],startYn+res[0]),cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 	1 , cv.LINE_AA)
							# Noplate_img = tempimg[res[0]:res[1]+res[3],res[1]:res[0]+res[2]]
							pts= [startXn+res[1],startYn+res[0],endXn-res[1]+res[2],endYn-res[0]+res[3]]
							# base=os.path.basename(l)
							# det_data=[base,pts,"plate"]
							# detection_tsv(det_data,"a")
						except:
							pass
		if flag:
			Noplate_Ret = NpdObj.Check_if_NoPlate_Exist(img2)
			print('back')
			print(Noplate_Ret)
			print()
			if Noplate_Ret[0]:
				n=0
				print('heredown')
				for i,res in enumerate(Noplate_Ret[1]):
					cv.rectangle(img3, ( res[1],res[0]), (res[1]+res[2], res[0]+res[3]), (255, 178, 50), 7)
					cv.rectangle(img3, ( res[1],res[0]), (res[1]+res[2], res[0]+res[3]), (0, 0, 0), 3)
					print('heredown')
					skewObj=skw.newSkew()
					imgppp= img2[ res[0]:res[0]+res[3],res[1]:res[1]+res[2]]
					print('[skewimg]',imgppp.shape)
					Noplate_Skew_img=skewObj.StartProcess(imgppp)
					t1 = time.time()
					ret = CKOTOBJ.Detect_Characters(Noplate_Skew_img)
					cv.putText(img3 ,str(ret),(startXn+res[1],startYn+res[0]),cv.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 3 , cv.LINE_AA)
					# cv.putText(img3 ,str(ret),(startXn+res[1],startYn+res[0]),cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 		2 , cv.LINE_AA)
					# cv.putText(img3 ,str(ret),(startXn+res[1],startYn+res[0]),cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 	1 , cv.LINE_AA)
					pts=[res[1],res[0],res[1]+res[2],res[0]+res[3]]
					# base=os.path.basename(l)
					# det_data=[base,pts,"plate"]
					# detection_tsv(det_data,"a")
		result.write(img3)
		print('-----','Write : ',no)
		# cv.imshow("frame" , img)
		# cv.waitKey(0)
		# img2=cv.resize(img2,(400,300))
		# cv.imshow("frame2" , img2)
		# cv.waitKey(0)
			
	except Exception as e:
		print(e,e,e)
		pass

	# if no > 20:
	# 	break
cap.release() 
result.release() 
cv.destroyAllWindows() 
print(time.time()-ttt1)
print("The video was successfully saved") 