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
		self.AlexNet = keras.models.load_model(r'E:/0NewDev/SIH/SIH_APP_SERVER/SIH_SERVER//API/weights/DenseNet169_E10.hdf5')
		self.listOfLbl = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
	def predict(self,img):
		predictions = self.AlexNet.predict(img)[0]
		result_args = predictions.argsort()[-1]
		result = self.listOfLbl[result_args]
		print(' [ Pred ] ', result)
		print(' [ Acc  ] ', predictions[result_args])
		return (result,predictions[result_args])
		

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