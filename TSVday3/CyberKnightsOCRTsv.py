import cv2 
import argparse
import sys
import numpy as np
import os.path
import glob
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from tensorflow import keras
import time
import csv
import newSkew as skw

class Character_Detector:
	def __init__(self):
		self.confThreshold = 0.1 
		self.nmsThreshold = 0.1 
		self.inpWidth = 416  
		self.inpHeight = 416 
		classesfile1  = r'classes\classes2.names'
		self.modelConfiguration = r"cfgs\YoloV3SIH(Segmentation).cfg"
		self.modelWeights = r"E:\0NewDev\SIH\SIH_APP_SERVER\SIH_SERVER\\API\weights\YoloV3SIH(Segmentation)_final.weights"
		
		self.net = cv2.dnn.readNetFromDarknet(self.modelConfiguration, self.modelWeights)
		self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
		self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
		# self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
		# self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

		self.model = None
		self.Modelcnt = 0

	def Detect_Characters(self,frame):
		dl1 = time.time()

		print("*"*100)
		print("In chars-segment")
		print("*"*100)
		def select_char(arr):
			print('In select_char')
			for x in arr:
				if x[0].isdigit():
					continue
				else:
					if x==arr[0]:
						return (False , x[0])
					else:
						return (True , x[0])
			return (False , arr[0][0])

		def select_digit(arr):
			for x in arr:
				if x[0].isalpha():
					continue
				else:
					if x==arr[0]:
						return (False , x[0])
					else:
						return (True , x[0])
			return (False , arr[0][0])

		dt1 = time.time()

		self.blob = cv2.dnn.blobFromImage(frame, 1/255, (self.inpWidth, self.inpHeight), [0,0,0], 1, crop=False)
		self.net.setInput(self.blob)
		self.outs = self.net.forward(self.getOutputsNames())
		self.res = self.postprocess(frame)
		dt2 = time.time()
		print('[Get segments Time]',dt2-dt1)
		retVal = 0
		plate = ''
		plate_update = ''

		if self.res:
			### top,left,width,height,confidences1
			retVal = 1
			img = frame
			retVal = 1
			#heights arr
			harr = [y[3] for y in self.res]
			hAvg = sum(harr) / len(harr) # max(harr)#

			yarr = [y[0] for y in self.res]
			ymin = min(yarr)
			ymax = max(yarr)
			yDiff = abs(ymin - ymax)
			print(ymin,ymax, hAvg ,yDiff)

			Vehicle = None
			if yDiff < hAvg:
				Vehicle = 'car'
			elif yDiff > hAvg:
				Vehicle = 'bike'
			print(Vehicle)
			if Vehicle == 'car':
				self.res.sort(key = lambda x: x[1])

			elif Vehicle == 'bike':
				# HSRP Assumed
				self.res.sort(key = lambda x: x[0])
				y_up = []
				y_down = []
				sepPoint = (ymin+ymax)//2
				for r in self.res:
					if r[0] < sepPoint:
						y_up.append(r)
					else:
						y_down.append(r)

				y_up.sort(key = lambda x: x[1])
				y_down.sort(key = lambda x: x[1])
				self.res = []
				for i in y_up:
					self.res.append(i)
				for i in y_down:
					self.res.append(i)

				print("*"*100)
				print("[BIKE]",self.res)
				print("*"*100)

			arr_img =[]
			for i in range(len(self.res)):
				x,y,h,w,c_id,c = self.res[i]
				img_c = img[x:x+w,y:y+h]
				arr_img.append(img_c)
			plate , arr_pred= self.Recognition(arr_img)
			print(plate)
			plate_final = []
			if len(arr_pred) == 10:
				for j,pred in enumerate(arr_pred):
					if j in [0,1,4,5]:
						ret_l = select_char(pred)
						print('ret_l',ret_l)
						plate_final.append(ret_l[1])
					
					elif j in [2,6,7,8,9]:
						ret_l = select_digit(pred)
						print('ret_l',ret_l)
						plate_final.append(ret_l[1])
					else:
						plate_final.append(pred[0][0])
			elif len(arr_pred) == 11:
				for j,pred in enumerate(arr_pred):
					if j in [0,1,4,5,6]:
						ret_l = select_char(pred)
						print('ret_l',ret_l)
						plate_final.append(ret_l[1])
					
					elif j in [2,3,7,8,9,10]:
						ret_l = select_digit(pred)
						print('ret_l',ret_l)
						plate_final.append(ret_l[1])
					else:
						plate_final.append(pred[0][0])
			elif len(arr_pred) == 9:
				for j,pred in enumerate(arr_pred):
					if j in [0,1,4]:
						ret_l = select_char(pred)
						print('ret_l',ret_l)
						plate_final.append(ret_l[1])
					elif j in [2,5,6,7,8]:
						ret_l = select_digit(pred)
						print('ret_l',ret_l)
						plate_final.append(ret_l[1])
					else:
						plate_final.append(pred[0][0])
			else:
				print("Unique"*10,len(arr_pred))
				for j,pred in enumerate(arr_pred):
					plate_final.append(pred[0][0])
			dl2 = time.time()
			print('[Seg+Reco+process]',dl2-dl1)

			plate_update = ''.join(plate_final)
			print(plate , plate_update)
		return (plate_update)

	def getOutputsNames(self):
		self.layersNames = self.net.getLayerNames()
		return [self.layersNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
   
	def postprocess(self,frame):
		frameHeight = frame.shape[0]
		frameWidth = frame.shape[1]

		classIds = []
		confidences = []
		confidences1 = []
		boxes = []
		for out in self.outs:
			print("out.shape : ", out.shape)
			for detection in out:
				scores = detection[5:]
				classId = np.argmax(scores)
				confidence = scores[classId]
				if detection[4]>self.confThreshold:
					pass
				if confidence > self.confThreshold:
					confidences1.append(confidence)

					center_x = int(detection[0] * frameWidth)
					center_y = int(detection[1] * frameHeight)
					width = int(detection[2] * frameWidth)
					height = int(detection[3] * frameHeight)
					left = int(center_x - width / 2)
					top = int(center_y - height / 2)
					classIds.append(classId)
					confidences.append(float(confidence))
					boxes.append([left, top, width, height,classId,float(confidence)])

		left,width,top,height = '','','',''
		indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
		if len(indices) > 1:
			print('Multiple Noplate in Image')
		xxx = []
		for i in indices:
			i = i[0]
			box = boxes[i]
			left = box[0]
			top = box[1]
			width = box[2]
			height = box[3]
			classid = box[3]
			confidence = box[3]
			# print()
			xxx.append((top,left,width,height,classid,confidence))
		return (xxx)

		def drawPred(self,classId, conf, left, top, right, bottom):
			cv2.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 2)
			label1 = '%.2f' % conf
			if classes:
				assert(classId < len(classes))
				label = '%s' % (classes[classId])
				# print(forindex.index(label) ," : ", label1)
			labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
			top = max(top, labelSize[1])
			l,t,r,b = convert(frame.shape,(left,right,top,bottom))
			cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

		def convertToYolo(self, size, box):
			dw = 1./size[1]
			dh = 1./size[0]
			x = (box[0] + box[1])/2.0
			y = (box[2] + box[3])/2.0
			w = box[1] - box[0]
			h = box[3] - box[2]
			x = x*dw
			w = w*dw
			y = y*dh
			h = h*dh 
			return (x,y,w,h)

	def LoadKerasModel(self):
		ml1 = time.time()
		print("Model Lode Called")
		self.model_Res = keras.models.load_model(r'E:\0NewDev\SIH\SIH_APP_SERVER\SIH_SERVER\API\weights\ResNet_Epoch_20.hdf5')
		self.model_ResV2 = keras.models.load_model(r'E:\0NewDev\SIH\SIH_APP_SERVER\SIH_SERVER\API\weights\ResNetV2_Epoch_20.hdf5')
		self.model_Dense169 = keras.models.load_model(r'E:\0NewDev\SIH\SIH_APP_SERVER\SIH_SERVER\API\weights\DenseNet169_E10.hdf5')

		ml2 = time.time()
		print('[Model Load Time]',ml2-ml1)

	def Recognition(self,arr_img):
		if self.Modelcnt == 0:
			self.Modelcnt+=1
			self.LoadKerasModel()

		lis1 = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
		batch_size = 128
		IMG_HEIGHT = 50
		IMG_WIDTH = 30
		ans = []
		ans2 = []
		for img_0 in arr_img:
			tt1 = time.time()
			try:
				img_1 = cv2.resize(img_0.copy(),(128,128))
				img_1 = np.asarray(img_1) 
				img_1 = img_1 / 255.0
				image1 = np.expand_dims(img_1, axis=0) 
				print(img_1.shape , image1.shape)

				predictions2 = self.model_Res.predict(image1).tolist()
				predictions3 = self.model_ResV2.predict(image1).tolist()
				predictions4 = self.model_Dense169.predict(image1).tolist()
				

				tt2= time.time()
				print("[TIME-Pred] ", tt2-tt1)
				predictions = [(predictions2[0][i]+predictions3[0][i])+predictions4[0][i]/3 for i in range(len(predictions2[0]))]
				predictions = np.asarray(predictions)

				result_args = predictions.argsort()[-5:][::-1]

				# print(result_args)
				ans2.append(((lis1[result_args[0]],predictions[result_args[0]]),
								(lis1[result_args[1]],predictions[result_args[1]]),
								(lis1[result_args[2]],predictions[result_args[2]]),
								(lis1[result_args[3]],predictions[result_args[3]]),
								(lis1[result_args[4]],predictions[result_args[4]])))
				ans.append(lis1[result_args[0]])

			except Exception as e:
				print(e)

		return (''.join(ans)  , ans2 )


if __name__ == '__main__':
	NpdObj = Character_Detector()
	lis = glob.glob(r'E:\0NewDev\SIH\OCRday2\*.jpg')

	font = cv2.FONT_HERSHEY_SIMPLEX
	ct = 0
	data = []
	for img_p in lis:
		print("*"*100)
		print("-  -"*25)
		print("*"*100)
		img = cv2.imread(img_p)
		skewObj=skw.newSkew()
		Noplate_Skew_img=skewObj.StartProcess(img)
		t1 = time.time()
		ret = NpdObj.Detect_Characters(Noplate_Skew_img)
		t2= time.time()
		print("[TIME] ", t2-t1)
		data.append([(img_p.split('\\')[-1]) , ret])
		# break
	with open('CyberKnights_OCR_test.tsv', 'w', newline='') as f_output:
		tsv_output = csv.writer(f_output, delimiter='\t')
		tsv_output.writerow(['image' , 'OCR'])
		for i in data:
			tsv_output.writerow(i)
		# xf = cv2.resize(img,(800,400))

		# cv2.imshow("Frame",xf)
		# cv2.waitKey(0)
		ct+=1
		
	