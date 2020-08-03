from django.shortcuts import render , redirect
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.http import HttpResponse ,HttpResponseRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate ,logout
from django.contrib.auth.mixins import LoginRequiredMixin
 
from API.forms import SignUpForm 

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics
 
from .forms import *  

import cv2
import json
import numpy as np
from scipy.spatial import distance as dist
from imutils import paths
from pprint import pprint
import time
import base64

import API.NoPlateDetector as NPD
import API.CharsSegmentReco as CHD
# import API.CharsDetector as CHD
# import API.SkewCorrection_and_Warp as skw
import API.newSkew as skw
 

NpdObj = NPD.No_Plate_Detector()
ChdObj = CHD.Character_Detector()
no = 0
frame_b64 = None
@api_view(["POST"])
def test(request, *args, **kwargs):
	try:
		t1e = time.time()
		global no,frame_b64
		no+=1
		handle_uploaded_file(request.FILES['Img_upload'])
		# handle_uploaded_file(request.FILES['upload'])
		img = cv2.imread(r'API\temp\\'+str(no)+'.jpg')
		img1= img.copy()
		Noplate_Ret = NpdObj.Check_if_NoPlate_Exist(img)
		Response_json = dict()
		Detecte_Plates_json  = dict()
		frame_b64 = None
		To_Draw = []
		if Noplate_Ret[0]:
			Response_json["No_Plate"] = True
			n=0
			for i,res in enumerate(Noplate_Ret[1]):
				No_Plate_Dict = dict()
				print('RES = >',res)
				Noplate_img = img[res[0]:res[0]+res[3],res[1]:res[1]+res[2]]
				skt1 = time.time()
				skewObj=skw.newSkew()
				Noplate_Skew_img=skewObj.StartProcess(Noplate_img)
				skt2 = time.time()
				print('[Skew Time]',skt2-skt1)
				Noplate_img_res       =	 ChdObj.Detect_Characters(Noplate_img)
				Noplate_Skew_img_res  =	 ChdObj.Detect_Characters(Noplate_Skew_img)

				x = ''
				No_Plate_Dict["FINAL_PRED"] = x

				Original_img_json = dict()
				Original_img_json["Result"] = Noplate_img_res[0]
				Original_img_json["Coord"] = res
				No_Plate_Dict["Original_img"] = Original_img_json


				Skew_img_json = dict()
				Skew_img_json["Result"] = Noplate_Skew_img_res[0]
				Skew_img_json["Coord"] = res
				No_Plate_Dict["Skew_img"] = Skew_img_json

				No_Plate_Dict["FINAL_PRED"] = Skew_img_json

				n+=1
				cv2.imwrite(r'C:\Users\M G DARJI\Desktop\temp\noplate'+str(no)+'-'+str(Noplate_img_res[0])+'-ORI.jpg',Noplate_img)
				n+=1
				cv2.imwrite(r'C:\Users\M G DARJI\Desktop\temp\noplate'+str(no)+'-'+str(Noplate_Skew_img_res[0])+'-skew.jpg',Noplate_Skew_img)
				 
				To_Draw.append((Noplate_Skew_img_res[0],res))
				Detecte_Plates_json['No_Plate_'+str(i+1)] = No_Plate_Dict
				# cv2.imwrite(r"API\static\Result\Res.jpg",img)
			DrawY= 0
			for i in range(len(To_Draw)):
				res = To_Draw[i][1]
				cv2.rectangle(img1, (res[1], res[0]), (res[1]+res[2], res[0]+res[3]), (255, 178, 50), 5)
				cv2.rectangle(img1, (res[1], res[0]), (res[1]+res[2], res[0]+res[3]), (0, 0, 0), 1)
			H,W,_ = img.shape
			n_H = 400
			n_W = W*400//H
			img1 = cv2.resize(img1,(n_W,n_H))
			for i in range(len(To_Draw)):
				label = To_Draw[i][0]
				
				cv2.rectangle(img1, (0,DrawY), (250,DrawY+50), (255, 178, 50), -1)
				cv2.rectangle(img1, (0,DrawY), (250,DrawY+50), (0, 0, 0), 5)
				cv2.putText(img1, label, (10,DrawY+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4)
				DrawY+=55

				# cv2.putText(img, label, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 4)
				# cv2.putText(img, label, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,255,0), 2)

				# img = cv2.imread(r"API\static\Result\Res.jpg")

			ret, frame_buff = cv2.imencode('.jpg', img1)
			frame_b64 =str( base64.b64encode(frame_buff))[2:-1]



			Response_json["Detecte_Plates"] = Detecte_Plates_json
			# reslis = list(Response_json.values())
			# score = []
			t2e = time.time()
			print("[REQUEST SERVE TIME]",t2e-t1e)
		else:
			Response_json["No_Plate"] = False

		print('*'*50)
		print(Response_json) 
		print('*'*50)
		return JsonResponse({'Key':Response_json})
		# return render(request, 'NoPlateDisplay.html', {'key':Response_json , 'img':frame_b64})
	except Exception as e:
		print(e," Error "*10)
		return JsonResponse({'Error':" ERROR :"+str(e)})
		# return render(request, 'result.html', {'p': facesNumber, 'img': frame_b64})
	finally:
		pass

def handle_uploaded_file(f):
	global no
	with open(r'API\temp\\'+str(no)+'.jpg', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

AnsRes = None
class Index(View):
	template = 'index.html'
	login_url = '/login/'

	def get(self, request):
		form = ImageUploadForm() 
		return render(request, self.template , {'form' : form}) 

	def post(self, request):
		# print('NoPlateResPage Get')
		# print('Form is_valid')
		try:
			form = ImageUploadForm(request.POST, request.FILES) 
			print(request.FILES)
			if form.is_valid(): 
				json_res = test(request)
				val = dict()
				global frame_b64					
				dix = json.loads((str(json_res.content)[2:-1]))
				print(dix)
				dix = dict(dix)
				plat = dict()
				detected = dix['Key']['No_Plate']
				if detected:
					AllKeys = list(dix['Key']['Detecte_Plates'].keys())
					print(AllKeys)
					for i,key in enumerate(AllKeys):
						print('[KEY]',key)
						val[key] = {'plate' : dix['Key']['Detecte_Plates'][key]['FINAL_PRED']['Result'],
									 'coord' : dix['Key']['Detecte_Plates'][key]['FINAL_PRED']['Coord'] }
		except Exception as e:
			val={'error':e}

		return render(request, 'NoPlateDisplay.html',{'RET': val,'img':frame_b64})



def success(request): 
	print('successfully uploaded')
	return HttpResponse('successfully uploaded  '+str(AnsRes)) 

class Login(View):
	template = 'login.html'

	def get(self, request):
		form = AuthenticationForm()
		return render(request, self.template, {'form': form})
 
	def post(self, request):
		form = AuthenticationForm(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		print(username , password)
		user = authenticate(request, username=username, password=password)
		print(user)
		if user is not None:
			login(request, user)
			print(user)
			return HttpResponseRedirect('/')
		else:
			return render(request, self.template, {'form': form})

class SignUp(View):
	template = 'SignUp.html'
	
	def get(self, request):
		form = SignUpForm()
		return render(request, self.template, {'form': form})

	def post(self, request): 
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/')
		else:
			return render(request, self.template, {'form': form})

class LogOut(View):
	def get(self, request):
		logout(request)
		# messages.info(request, "Logged out successfully!")
		return redirect('/')
	def post(self, request): 
		logout(request)
		# messages.info(request, "Logged out successfully!")
		return redirect('/')



class ApiInfo(View):
	"""docstring for ApiInfo"""
	template = 'ApiInfo.html'
	def get(self, request):
		# form = SignUpForm()
		return render(request, self.template)
	def post(self, request): 
		return render(request, self.template)
		
class AccountDetail(LoginRequiredMixin ,View):
	template = 'AccountDetail.html'
	def get(self, request):
		# form = SignUpForm()
		return render(request, self.template)
	def post(self, request): 
		# form = SignUpForm(request.POST)
		# if form.is_valid():
			# form.save()
			# username = form.cleaned_data.get('username')
			# raw_password = form.cleaned_data.get('password1')
			# user = authenticate(username=username, password=raw_password)
			# login(request, user)
			# return redirect('/')
		# else:
			return render(request, self.template)