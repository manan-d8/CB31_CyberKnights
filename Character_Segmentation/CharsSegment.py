import cv2 
import numpy as np
import os
import glob
import time
classes = []
class Char_Seg:
	def __init__(self):
		self.confThreshold = 0.1 
		self.nmsThreshold = 0.1 
		self.inpWidth = 416  
		self.inpHeight = 416 
		self.classes  = r'Classes\classes.names'
		with open(self.classes, 'rt') as f:
			self.classes = f.read().rstrip('\n').split('\n')
		global classes
		classes = self.classes
		self.modelConfiguration = r"Cfg\YoloV3SIH(chars-segment).cfg"
		self.modelWeights = r"Weights\YoloV3SIH(chars-segment)_final.weights"
		self.net = cv2.dnn.readNetFromDarknet(self.modelConfiguration, self.modelWeights)
		try :
			self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
			self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
		except Exception as e:
			Print('[ INFO ]', 'Cuda Not Available , Using Cpu')
			self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
			self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


	def Check_if_Char_Exist(self,frame):

		nd1= time.time()

		self.blob = cv2.dnn.blobFromImage(frame, 1/255, (self.inpWidth, self.inpHeight), [0,0,0], 1, crop=False)
		self.net.setInput(self.blob)
		self.outs = self.net.forward(self.getOutputsNames())
		self.res = self.postprocess(frame)

		nd2= time.time()

		print('[ Time ]','[NoPlate Detection Time]',nd2-nd1)
		retVal = 0
		if self.res != []:
			retVal = 1
		return (retVal,self.res)

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
			for detection in out:
				scores = detection[5:]
				classId = np.argmax(scores)
				confidence = scores[classId]
				if detection[4] > self.confThreshold:
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
					boxes.append([left, top, width, height,classId,confidence])

		left,width,top,height = '','','',''
		
		indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)

		noPlates = []
		for i in indices:
			i = i[0]
			box 	= boxes[i]
			left 	= box[0]
			top		= box[1]
			width	= box[2]
			height	= box[3]
			classId	= box[4]
			ConfScore	= box[5]
			noPlates.append((top,left,width,height,classId,ConfScore))
		return noPlates


if __name__ == '__main__':
	no = 0
	segObj = Char_Seg()
	img_lis = glob.glob(r'Test_Images\\*.jpg')
	for img_path in img_lis:
		no += 1
		frame = cv2.imread(img_path)
		ret = segObj.Check_if_Char_Exist(frame)
		H,W,_ = frame.shape
		chars = ret[1]
		for char in chars:
			print(' [ Acc  ] ' , str(char[5]))
			frame = cv2.rectangle(frame, (char[1], char[0]), (char[1]+char[2], char[0]+char[3]), (0, 0, 0), 2)
			frame = cv2.rectangle(frame, (char[1], char[0]), (char[1]+char[2], char[0]+char[3]), (255, 178, 50), 1)
			cv2.putText(frame,str( classes[char[4]]), (char[1], char[0]), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255), 1 , cv2.LINE_AA)
		if H > W:
			n_H = 500
			n_W = W*500//H
		else:
			n_W = 500
			n_H = H*500//W
		frame = cv2.resize(frame,(n_W,n_H))
		cv2.imwrite('Results/CharSeg'+str(no)+'.jpg',frame)
		cv2.imshow('Output Frame' , frame)
		cv2.waitKey(0)