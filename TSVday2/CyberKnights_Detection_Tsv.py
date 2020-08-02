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
NpdObj = NPD.No_Plate_Detector()
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
for l in tqdm(lis):
	classname=""
	pts=[]
	try:
		no+=1    
		img = cv.imread(l)
		img2 = img.copy()
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
				print(startX, startY, endX, endY)

				startXn = W*startX//w
				startYn = H*startY//h
				endXn    = W*endX//w
				endYn    =H*endY//h

				print(startXn, startYn, endXn, endYn)

				img2 = cv.rectangle(img2, (startXn, startYn), (endXn, endYn), (255, 178, 50), 10)
				pts=[startXn,startYn,endXn,endYn]
				classname=CLASSES[idx]
				base=os.path.basename(l)
				det_data=[base,pts,classname]
				detection_tsv(det_data,"a")
				tempimg = img2[startYn:endYn , startXn:endXn]
				Noplate_Ret = NpdObj.Check_if_NoPlate_Exist(tempimg)
				print('back')
				print(Noplate_Ret)
				if Noplate_Ret[0]:
					n=0
					flag = False
					for i,res in enumerate(Noplate_Ret[1]):
						cv.rectangle(img2, ( startXn+res[1],startYn+res[0]), (startXn+ 	res[1]+res[2], startYn+res[0]+res[3]), (255, 178, 50), 20)
						# Noplate_img = tempimg[res[0]:res[1]+res[3],res[1]:res[0]+res[2]]
						pts= [startXn+res[1],startYn+res[0],endXn-res[1]+res[2],endYn-res[0]+res[3]]
						base=os.path.basename(l)
						det_data=[base,pts,"plate"]
						detection_tsv(det_data,"a")
		if flag:
			Noplate_Ret = NpdObj.Check_if_NoPlate_Exist(img2)
			print('back')
			print(Noplate_Ret)
			if Noplate_Ret[0]:
				n=0
				for i,res in enumerate(Noplate_Ret[1]):
					cv.rectangle(img2, ( res[1],res[0]), (res[1]+res[2], res[0]+res[3]), (0, 255, 0), 15)
					# Noplate_img = tempimg[res[0]:res[1]+res[3],res[1]:res[0]+res[2]]
					pts=[res[1],res[0],res[1]+res[2],res[0]+res[3]]
					base=os.path.basename(l)
					det_data=[base,pts,"plate"]
					detection_tsv(det_data,"a")
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

# 