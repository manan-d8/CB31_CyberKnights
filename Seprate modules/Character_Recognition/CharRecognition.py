import cv2 
import numpy as np
import os
import glob
import time
# import tensorflow as tf
from tensorflow import keras
classes = []

class Char_recognition():
	def __init__(self):
		self.call = 0
		self.listOfLbl = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
	def loadmodel(self):
		print('model load')
		## self.AlexNet = keras.models.load_model(r'Character_Recognition/Weights/AlexNet_char_best_model-50.hdf5')
		self.model_Res = keras.models.load_model(r'E:\0NewDev\SIH\SIH_APP_SERVER\SIH_SERVER\API\weights\ResNet_Epoch_20.hdf5')
		self.model_ResV2 = keras.models.load_model(r'E:\0NewDev\SIH\SIH_APP_SERVER\SIH_SERVER\API\weights\ResNetV2_Epoch_20.hdf5')
		self.model_Dense169 = keras.models.load_model(r'E:\0NewDev\SIH\SIH_APP_SERVER\SIH_SERVER\API\weights\DenseNet169_E10.hdf5')
	def predict(self,img):
		if self.call == 0:
			self.loadmodel()
		self.call+=1

		predictions2 = self.model_Res.predict(img).tolist()
		predictions3 = self.model_ResV2.predict(img).tolist()
		predictions4 = self.model_Dense169.predict(img).tolist()

		predictions = [(predictions2[0][i]+predictions3[0][i])+predictions4[0][i]/3 for i in range(len(predictions2[0]))]
		predictions = np.asarray(predictions)


		result_args = predictions.argsort()[-5:][::-1]

		# print(result_args)
		val1 =  (((self.listOfLbl[result_args[0]],predictions[result_args[0]]),
						(self.listOfLbl[result_args[1]],predictions[result_args[1]]),
						(self.listOfLbl[result_args[2]],predictions[result_args[2]]),
						(self.listOfLbl[result_args[3]],predictions[result_args[3]]),
						(self.listOfLbl[result_args[4]],predictions[result_args[4]])))
		return self.listOfLbl[result_args[0]] , val1



	def Reco_pred(self , img , chars):
		arr_pred = []
		chars = chars.sort(key = lambda x: x[0])

		for char in chars:
			print(img.shape )
			imgcv = img[char[0]:char[0]+char[3] , char[1]:char[1]+char[2] ]   #(char[1], char[0]), (char[1]+char[2], char[0]+char[3]
			print(imgcv.shape)
			imgcv = cv2.resize(imgcv,(128,128))
			imgcv = np.asarray(imgcv) 
			imgcv = imgcv / 255.0
			imgcv = np.expand_dims(imgcv, axis=0) 

			a, b= self.predict(imgcv)
			arr_pred.append(b)

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
				
				# elif j in [2,len(arr_pred)-4,len(arr_pred)-3,len(arr_pred)-2,len(arr_pred)-1]:
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
				
				# elif j in [2,len(arr_pred)-4,len(arr_pred)-3,len(arr_pred)-2,len(arr_pred)-1]:
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
		print(plate_final)

		# print(str(ret)+':'+(str(acc)[:5]))


if __name__ == '__main__':
	no = 0
	RecoObj = Char_recognition()
	img_lis = glob.glob(r'Test_Images\\*.jpg')
	for img_path in img_lis:
		no += 1
		imgcv = cv2.imread(img_path)
		imgcv = cv2.resize(imgcv,(128,128))
		img = np.asarray(imgcv) 
		img = img / 255.0
		img = np.expand_dims(img, axis=0) 
		t1  = time.time()
		ret,acc = RecoObj.predict(img)
		print(' [ Time ] ',' [ Recognition Time ]',time.time()-t1)
		cv2.putText(imgcv ,str(ret)+':'+(str(acc)[:5]), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3 , cv2.LINE_AA)
		cv2.putText(imgcv ,str(ret)+':'+(str(acc)[:5]), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 		2 , cv2.LINE_AA)
		cv2.putText(imgcv ,str(ret)+':'+(str(acc)[:5]), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 	1 , cv2.LINE_AA)
		cv2.imwrite('Results/CharReco'+str(no)+'.jpg',imgcv)
		cv2.imshow('Output Frame' , imgcv)
		cv2.waitKey(0)