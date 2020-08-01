import cv2
import json
import os,glob
import time
import numpy as np
from Character_Recognition import CharRecognition as CR
from Character_Segmentation import CharsSegment as CS
import newSkew as skw
 

segObj = CS.Char_Seg()
RecoObj = CR.Char_recognition()
Load = True

def OCR_FROM_IMAGE(img):
	t1 = time.time()
	skewObj=skw.newSkew()
	Noplate_Skew_img=skewObj.StartProcess(img)
	ret = segObj.Check_if_Char_Exist(Noplate_Skew_img)
	chars = ret[1]
	plate  = RecoObj.Reco_pred(Noplate_Skew_img,chars)


lis = glob.glob(r"Test_imgs\*.jpg")
with open('output.tsv', 'w', newline='') as f_output:
    tsv_output = csv.writer(f_output, delimiter='\t')
	for i in lis:
		print("*"*100,i)
		img = cv2.imread(i) 
		plate = OCR_FROM_IMAGE(img)
		tsv_output = [i.split('/')[-1] , plate]
		tsv_output.writerow(data)
	# break
