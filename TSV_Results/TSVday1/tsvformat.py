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
path = r"<path>*.jpg"
#path2 = r"E:\0NewDev\SIH\Datasetes\crop"
lis = glob.glob(path)
no=0
import xml.etree.cElementTree as ET
from PIL import Image
import csv        

ANNOTATIONS_DIR_PREFIX = "annotation"

DESTINATION_DIR = "converted_labels"

confThreshold = 0.5  #Confidence threshold
nmsThreshold = 0.4  #Non-maximum suppression threshold
inpWidth = 416 
inpHeight = 416
classes = None
counter = 0
CLASSES = ["background","car","bicycle","motorbike","bus"]
# CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
#     "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
#     "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
#     "sofa", "train", "tvmonitor"]
#net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
conf = Conf("config.json")
net = cv.dnn.readNetFromCaffe(conf["prototxt_path"],conf["model_path"])
# net = cv.dnn.readNetFromCaffe('no_bn.caffemodel','no_bn.prototxt')

net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


conf = Conf("config.json")
def detection_tsv(data,w_or_a):
	with open('det_output.tsv', w_or_a, newline='') as f_output:
		tsv_output = csv.writer(f_output, delimiter='\t')
		tsv_output.writerow(data)

def ocr_tsv(data,w_or_a):
	with open('ocr_output.tsv', w_or_a, newline='') as f_output:
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
	tree.write("{}/{}.xml".format(r'C:/Users/bhaga/Desktop/TrainDataSih/', file_prefix))
no =0
data_ocr=["Image","OCR"]
ocr_tsv(data_ocr,"w")
detection_ocr=["Image","BBox","Label"]
detection_tsv(detection_ocr,"w")
pts=[]
classname=""
for l in tqdm(lis):
	classname=""
	pts=[]
	# copyfile(l, path2+'\\'+str(no)+'.jpg')
	try:
		no+=1    
		img = cv.imread(l)
		img = imutils.resize(img, width=conf["frame_width"])
		# img = img[(height//3):,:]
		# print("==================================>",img.shape[1],img.shape[0])
		counter+=1
		# Create a 4D blob from a frame.
		blob = cv.dnn.blobFromImage(img, size=(300, 300),ddepth=cv.CV_8U)
		net.setInput(blob, scalefactor=1.0/127.5, mean=[127.5,127.5, 127.5])
		detections = net.forward()
		vocl = []
		# W,H = 400,300
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

				# if the class label is not a car, ignore it
				# print(' [Class] ' , CLASSES[idx] , idx , confidence)
				if CLASSES[idx] not in[ "background","car","motorbike","bus"]:
					continue
#                 print(' [ label ] ',CLASSES[idx])
				(H, W) = img.shape[:2]
				box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
				(startX, startY, endX, endY) = box.astype("int")
				H,W,_ = img.shape
				cv.rectangle(img, (startX, startY), (endX, endY), (255, 178, 50), 10)

				newimg = img[startY:endY , startX:endX]
				print(newimg.shape)
				
				fPathTxt = l[36:-4]

#                 print(startX, startY, endX, endY)
				#vocl.append((CLASSES[idx] ,startX, startY, endX, endY))
				pts=[startX,startY,endX,endY]
				classname=CLASSES[idx]


				base=os.path.basename(l)
				fname=base.rsplit('.',1)[0]
				#data_ocr=[fname,##passLPcharacterstringHere]
				#ocr_tsv(data_ocr)
				print(fname)
				print(pts)
				print(classname)
				det_data=[fname,pts,classname]
				detection_tsv(det_data,"a")
		#cv.imwrite(l,img)
	   
		#create_file(fPathTxt, W, H, vocl)
		#create_tsv(fPathTxt, W, H, vocl)
		
	except Exception as e:
		pass

	cv.imshow('f',img)
	cv.waitKey(0)
	# if no > 10:
	#     break

