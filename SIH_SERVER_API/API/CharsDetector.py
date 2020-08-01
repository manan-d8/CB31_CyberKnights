import cv2 
import argparse
import sys
import numpy as np
import os.path
import glob
import os


# modelConfiguration2 = r"E:\0NewDev\New\WeightsAndCfg\YoloV3SIH(chars).cfg"
# modelWeights2 = r"E:\0NewDev\New\WeightsAndCfg\YoloV3SIH(chars)_19000.weights"
# classesfile2  = r'mainapi\classes2.names'
# with open(classesfile2, 'rt') as f:
#     classes2 = f.read().rstrip('\n').split('\n')
# net2 = cv2.dnn.readNetFromDarknet(modelConfiguration2, modelWeights2)
# net2.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net2.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
class Character_Detector:
	def __init__(self ):
		self.confThreshold = 0.1
		self.nmsThreshold = 0.1 
		self.inpWidth = 416  
		self.inpHeight = 416 

		# self.classesFile = classesfile2
		# self.classes = classes2
		# self.modelConfiguration = modelConfiguration2
		# self.modelWeights = modelWeights2
		# self.net = net2


		classesfile2  = r'API\classes\classes2.names'
		with open(classesfile2, 'rt') as f:
			classes2 = f.read().rstrip('\n').split('\n')
		self.classes = classes2
		self.modelConfiguration = r"E:\0NewDev\New\WeightsAndCfg\YoloV3SIH(chars).cfg"
		self.modelWeights = r"E:\0NewDev\New\WeightsAndCfg\YoloV3SIH(chars)_19000.weights"
		self.net = cv2.dnn.readNetFromDarknet(self.modelConfiguration, self.modelWeights)
		self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
		self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)


	def Detect_Characters(self,frame):
		self.CharDetectList = []
		try:
			self.blob = cv2.dnn.blobFromImage(frame, 1/255, (self.inpWidth, self.inpHeight), [0,0,0], 1, crop=False)
		except:
			return (0,'')
		self.net.setInput(self.blob)
		self.outs = self.net.forward(self.getOutputsNames())
		self.postprocess(frame)
		self.res = []
		retVal = 0
		str1 = ''
		if self.CharDetectList != []:
			retVal = 1
			harr = ([y[4] for y in self.CharDetectList])
			hAvg = max(harr)#sum(harr) / len(harr)
			yarr = [y[2] for y in self.CharDetectList]
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
				lst = sorted(self.CharDetectList, key=lambda x: x[1], reverse=False)
				for i in lst:
					str1+=str(i[0])
			elif Vehicle == 'bike':
				y_up = []
				y_down = []
				for i in self.CharDetectList :
					if abs(i[2]-ymin) < abs(i[2]-ymax):
						y_up.append(i)
					else:
						y_down.append(i)
				lst1 = sorted(y_up, key=lambda x: x[1], reverse=False)
				lst2 = sorted(y_down, key=lambda x: x[1], reverse=False)
				for i in lst1:
					str1+=str(i[0])
				for i in lst2:
					str1+=str(i[0])

		print(self.CharDetectList)
		return (retVal,str1)
		# t, _ = net.getPerfProfile()
		# label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())

	def getOutputsNames(self):
		self.layersNames = self.net.getLayerNames()
		return [self.layersNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
   
	def postprocess(self,frame):
		frameHeight = frame.shape[0]
		frameWidth = frame.shape[1]

		classIds = []
		confidences = []
		boxes = []
		for out in self.outs:
			print("out.shape : ", out.shape)
			for detection in out:
				scores = detection[5:]
				classId = np.argmax(scores)
				confidence = scores[classId]
				if detection[4]>self.confThreshold:
					#print(detection[4], " - ", scores[classId], " - th : ", confThreshold)
					#print(detection)
					pass
				if confidence > self.confThreshold:
					center_x = int(detection[0] * frameWidth)
					center_y = int(detection[1] * frameHeight)
					width = int(detection[2] * frameWidth)
					height = int(detection[3] * frameHeight)
					left = int(center_x - width / 2)
					top = int(center_y - height / 2)
					classIds.append(classId)
					confidences.append(float(confidence))
					boxes.append([left, top, width, height])

		left,width,top,height = '','','',''
		indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
		if len(indices) > 1:
			print('Multiple Noplate in Image')
		for i in indices:
			i = i[0]
			box = boxes[i]
			left = box[0]
			top = box[1]
			width = box[2]
			height = box[3]
			self.CharDetectList.append((self.classes[classIds[i]],left,top,width,height))
			#l,t,r,b = self.convert(frame.shape,(left,right,top,bottom))
			#drawPred(classIds[i], confidences[i], left, top, left + width, top + height,file2)

		def drawPred(self,classId, conf, left, top, right, bottom):
			cv2.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 2)
			label1 = '%.2f' % conf
			if classes:
				assert(classId < len(classes))
				label = '%s' % (classes[classId])
				print(forindex.index(label) ," : ", label1)
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

if __name__ == '__main__':

	modelConfiguration = r"E:\0NewDev\New\WeightsAndCfg\YoloV3SIH(Noplate).cfg"
	modelWeights = r"E:\0NewDev\New\WeightsAndCfg\YoloV3SIH(Noplate)_5000.weights"
	classesfile  = r'classes2.names'
	confThreshold = 0.1 
	nmsThreshold = 0.1 
	NpdObj = No_Plate_Detector(modelConfiguration,modelWeights,classesfile,confThreshold,nmsThreshold)
	cap=cv2.VideoCapture(r"E:\0NewDev\New\testNOplate\New folder\ame133.jpg")
	ret,frame=cap.read()
	if ret:
		ret = NpdObj.Check_if_NoPlate_Exist(frame)
		if ret[0]:
			res = ret[1]
			cv2.imwrite('plate.jpg',frame[res[0]:res[0]+res[3],res[1]:res[1]+res[2]])
	