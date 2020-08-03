import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk ,Image
import cv2
import sys
import numpy as np
import os.path
import os
import conf
import imutils
import vehicles
import  time
import queue 
import threading
import requests
from pprint import pprint
import json
# from mysql.connector import MySQLConnection, Error
# import mysql.connector
from datetime import datetime
import random
import json
import Email
import DbHandle as DB

Font_Name = "Helvetica"
# helv36 = Font(family="Helvetica",size=36,weight="bold")
Base_Dir = os.path.dirname(os.path.abspath(__file__))
print(Base_Dir)
visiterFolder = '/VisitorStored/'

# Theme Clrs
clr1 = "#0C0D0B"
clr2 = "#262624"
clr3 = "#FFC54A"

# clr1 = "#0C0D0B"
# clr2 = "#001822"
# clr3 = "#9FB18F"


# Global Vars
Pause_main= False
DB_H = None
Video_Path = r'test2.mp4'
Video_Capture = None
Log_Canvas = None
Frame_fullRes = None
Frame_1 = None
Que = None
root = None
detector = None
MailOBJ = None
VisitorsListZoom = []
# Detector Lines
with open('Frame_coord.json') as f:
  data = json.load(f)
print(dict(data))
Line_Up1    = data['Line_Up1']
Line_Up2    = data['Line_Up2']
Line_Down1  = data['Line_Down1']
Line_Down2  = data['Line_Down2']
Up_Limit    = data['Up_Limit']
Down_Limit  = data['Down_Limit']

Status_Lbl = None
Up_Count_Lbl = None
Down_Count_Lbl = None
Visitor_Count_Lbl = None
Api_Res_Frm = None
Headlbl = None

def donothing():
	global Headlbl
	Headlbl
def sendmails():
	global MailOBJ
	MailOBJ.Sendmails()
	


class MainApp(tk.Frame):
	def __init__(self,parent,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		MenuBar
		TopFrame(self,bg=clr1,relief=tk.RIDGE,bd=2).pack(side = tk.TOP,fill = tk.X)
		MidFrame(self,bg=clr2,relief=tk.RIDGE,bd=2).pack(side = tk.TOP,fill = tk.BOTH ,expand=True)
		BottomFrame(self,bg=clr2,relief=tk.RIDGE,bd=1).pack(side = tk.BOTTOM,fill = tk.X)

	def __del__(self):
		print('App Closed!')

class MenuBar(tk.Menu):
	def __init__(self,parent,*args,**kwargs):
		tk.Menu.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		filemenu = tk.Menu(self, tearoff=0)
		filemenu.add_command(label="New", command=donothing)
		filemenu.add_command(label="Open Video", command=self.openVideo)
		filemenu.add_command(label="Open Camera", command=self.openCam)
		filemenu.add_command(label="Save as...", command=donothing)
		filemenu.add_command(label="Close", command=donothing)

		filemenu.add_separator()

		filemenu.add_command(label="Exit", command=root.quit)
		self.add_cascade(label="File", menu=filemenu)

		editmenu = tk.Menu(self, tearoff=0)
		editmenu.add_command(label="Edit Lines", command=self.openEditLineWindow)
		editmenu.add_separator()
		editmenu.add_command(label="Send Mails", command=sendmails)
		# editmenu.add_command(label="Copy", command=donothing)
		# editmenu.add_command(label="Paste", command=donothing)
		# editmenu.add_command(label="Delete", command=donothing)
		# editmenu.add_command(label="Select All", command=donothing)

		self.add_cascade(label="Edit", menu=editmenu)
		helpmenu = tk.Menu(self, tearoff=0)
		helpmenu.add_command(label="Help Index", command=donothing)
		helpmenu.add_command(label="About...", command=donothing)
		self.add_cascade(label="Help", menu=helpmenu)

	def openEditLineWindow(self):
		newWindow = EditLinesWindow(root,bg=clr2) 

	def openCam(self):
		global Video_Capture
		Video_Capture.reload_video(0)       
	def openVideo(self):
		filename =  filedialog.askopenfilename(initialdir = "/home/manand8/dev/sih/SIH_APP_CLIENT",title = "Select file",filetypes = (("MP4 File","*.mp4"),("all files","*.*")))
		print (' [ SELECTED VIDEO ] ',filename)
		global Video_Capture
		Video_Capture.reload_video(filename)

class TopFrame(tk.Frame):
	def __init__(self,parent,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		global Headlbl
		Heading = "Vehicle Monitoring"
		Heading = "ऑटोमेटिक व्हीकल मॉनिटरिंग सिस्टम"
		Headlbl = mylbl(self, text= Heading,bg=clr1, fg=clr3, font=('Arial', 30,"bold"),relief=tk.RAISED,bd=3)
		Headlbl. pack(fill=tk.X)

class MidFrame(tk.Frame):
	def __init__(self,parent,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		MidLeftFrame(self,bg=clr2,relief=tk.RIDGE,bd=1).pack(side = tk.LEFT,fill = tk.Y)
		MidRightFrame(self,bg=clr2,relief=tk.RIDGE,bd=1).pack(side = tk.RIGHT,fill = tk.BOTH, expand = True)

class MidLeftFrame(tk.Frame):
	def __init__(self,parent,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		MidLeftTopFrame(self,bg=clr2,relief=tk.RIDGE,bd=1).pack(side = tk.TOP,fill = tk.Y)       
		global Log_Frame
		Log_Frame = MidLeftBottomFrame(self,bg=clr2,relief=tk.RIDGE,bd=1)
		Log_Frame.pack(side = tk.TOP,fill = tk.BOTH , expand = False)

class MidLeftTopFrame(tk.Frame):
	def __init__(self,parent,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		VideoFrame(self,bg=clr2).pack(side = tk.TOP,fill = tk.BOTH)

class MidLeftBottomFrame(tk.Frame):
	def __init__(self,parent,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		MidRightRightTopFrame(self,bg=clr2,relief=tk.RIDGE,bd=1).pack(side = tk.TOP,fill = tk.BOTH, expand = False)
		Heading = 'Vehicle Detection Log'
		mylbl(self, text= Heading,bg=clr1, fg=clr3, font=(Font_Name, 15),relief=tk.RIDGE,bd=1).pack(side = tk.TOP , fill=tk.X)
		# global Log_Frame
		global Log_Canvas
		self.canvas=tk.Canvas(self,bg=clr2)
		Log_Canvas=tk.Frame(self.canvas,bg=clr2)
		myscrollbar=tk.Scrollbar(self,orient="vertical",command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=myscrollbar.set)

		myscrollbar.pack(side=tk.RIGHT,fill=tk.Y)
		self.canvas.pack(side=tk.BOTTOM,fill = tk.BOTH)
		self.canvas.create_window((0,0),window=Log_Canvas,anchor='nw')
		Log_Canvas.bind("<Configure>",self.myfunction)
		self.canvas.configure(scrollregion=self.canvas.bbox("all"),height=120)
		Log_Canvas.grid_columnconfigure(0, weight=1, uniform="fred")
		Log_Canvas.grid_columnconfigure(1, weight=1, uniform="fred")
		Log_Canvas.grid_columnconfigure(2, weight=1, uniform="fred")
		# Log_Canvas.grid_columnconfigure(3, weight=1, uniform="fred")
		mylbl(Log_Canvas, text= "Vehicle Type",     bg=clr2, fg=clr3, font=(Font_Name, 15)).grid(row=0,column=0)
		mylbl(Log_Canvas, text= "ID",       bg=clr2, fg=clr3, font=(Font_Name, 15)).grid(row=0,column=1)
		mylbl(Log_Canvas, text= "Direction",bg=clr2, fg=clr3, font=(Font_Name, 15)).grid(row=0,column=2)
		mylbl(Log_Canvas, text= "Time Stamp",       bg=clr2, fg=clr3, font=(Font_Name, 15)).grid(row=0,column=3)

		self.width=self.winfo_width()
		self.height=self.winfo_height()


	def myfunction(self,event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"),height=100)




class MidRightFrame(tk.Frame):
	def __init__(self,parent,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		# MidRightLeftFrame(self,bg=clr2,relief=tk.RIDGE,bd=1).grid(row=0,column=0)
		# MidRightLeftFrame(self,bg=clr2,relief=tk.RIDGE,bd=1).pack(side = tk.LEFT,fill = tk.BOTH, expand = True)
		# MidRightRightFrame(self,bg=clr2,relief=tk.RIDGE,bd=1).grid(row=0,column=1)
		# self.grid_columnconfigure(0, weight=1, uniform="fred")
		# self.grid_columnconfigure(1, weight=1, uniform="fred")
		MidRightRightFrame(self,bg=clr2,relief=tk.RIDGE,bd=1).pack(side = tk.RIGHT,fill = tk.BOTH, expand = True)

class MidRightLeftFrame(tk.Frame):
	def __init__(self,parent,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.pa1rent = parent
		Heading = 'Server(noPlate) Detection Log'
		mylbl(self, text= Heading,bg=clr1, fg=clr3, font=(Font_Name, 10),relief=tk.RIDGE,bd=1).pack(side = tk.TOP , fill=tk.X)
		global Api_Res_Frm
		Api_Res_Frm = myFrm(self,bg=clr2,relief=tk.RIDGE,bd=1)
		Api_Res_Frm.pack(side = tk.TOP,fill = tk.BOTH, expand = False)

class MidRightRightFrame(tk.Frame):
	def __init__(self,parent,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		# Heading = 'Vehicle Counts'
		# mylbl(self, text= Heading,bg=clr1, fg=clr3, font=(Font_Name, 10),relief=tk.RIDGE,bd=1).pack(side = tk.TOP , fill=tk.X)
		
		Heading = 'Visitors Details...'
		mylbl(self, text= Heading,bg=clr1, fg=clr3, font=(Font_Name, 25),relief=tk.RIDGE,bd=1).pack(side = tk.TOP , fill=tk.X)
		# MidRightRightTopFrame(self,bg=clr2,relief=tk.RIDGE,bd=1).pack(side = tk.TOP,fill = tk.BOTH, expand = False)
		MidRightRightMidFrame(self,bg=clr2,relief=tk.RIDGE,bd=1).pack(side = tk.TOP,fill = tk.BOTH, expand = False)
		MidRightRightBottomFrame(self,bg=clr2,relief=tk.RIDGE,bd=1).pack(side = tk.BOTTOM,fill = tk.BOTH, expand = True)

class MidRightRightTopFrame(tk.Frame):
	def __init__(self,parent,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		global Up_Count_Lbl,Down_Count_Lbl
		# Heading = 'Vehicle Counting...'
		# mylbl(self, text= Heading,bg=clr1, fg=clr3, font=(Font_Name, 25),relief=tk.RIDGE,bd=1).pack(side = tk.TOP , fill=tk.X)
		
		upfrm = myFrm(self,bg=clr1)

		mylbl(upfrm, text= 'Going UP   : ',bg=clr1, fg=clr3, font=(Font_Name, 10),relief=tk.RIDGE,bd=1).grid(row=0,column=0,sticky='nsew',padx=2,pady=2)
		Up_Count_Lbl = mylbl(upfrm, text= '0',bg=clr2, fg=clr3, font=(Font_Name, 20),relief=tk.RIDGE,bd=1)
		Up_Count_Lbl.grid(row=0,column=1,sticky='nsew',padx=2,pady=2)
		# Up_Count_Lbl.columnconfigure(0, weight=1)

		mylbl(upfrm, text= 'Going DOWN : ',bg=clr1, fg=clr3, font=(Font_Name, 10),relief=tk.RIDGE,bd=1).grid(row=0,column=2,sticky='nsew',padx=2,pady=2)
		Down_Count_Lbl =  mylbl(upfrm, text= '0',bg=clr2, fg=clr3, font=(Font_Name, 20),relief=tk.RIDGE,bd=1)
		Down_Count_Lbl.grid(row=0,column=3,sticky='nsew',padx=2,pady=2)
		# Down_Count_Lbl.columnconfigure(0, weight=1)
		# upfrm.grid_columnconfigure(0, weight=1)
		upfrm.grid_columnconfigure(0, weight=1, uniform="fred")
		upfrm.grid_columnconfigure(1, weight=1, uniform="fred")
		upfrm.grid_columnconfigure(2, weight=1, uniform="fred")
		upfrm.grid_columnconfigure(3, weight=1, uniform="fred")
		upfrm.pack(side = tk.TOP , fill=tk.X, expand = True,padx=2,pady=2)


class MidRightRightMidFrame(tk.Frame):
	def __init__(self,parent,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		global Visitor_Count_Lbl
		visiterfrm = myFrm(self,bg=clr1)
		mylbl(visiterfrm, text= ' Current Visitors : ',bg=clr1, fg=clr3, font=(Font_Name, 20),relief=tk.RIDGE,bd=1).grid(row=0,column=0,sticky='nsew',padx=2,pady=4)
		Visitor_Count_Lbl = mylbl(visiterfrm, text= '0',bg=clr1, fg=clr3, font=(Font_Name, 20),relief=tk.RIDGE,bd=1 )
		Visitor_Count_Lbl.grid(row=0,column=1,sticky='nsew',padx=2,pady=4)  
		visiterfrm.grid_columnconfigure(0, weight=1, uniform="fred")
		visiterfrm.grid_columnconfigure(1, weight=1, uniform="fred")
		visiterfrm.pack(side = tk.TOP , fill=tk.X, expand = True)

class MidRightRightBottomFrame(tk.Frame):
	def __init__(self,parent,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent

		self.visitorlogFrm = myFrm(self,bg=clr1  ,relief=tk.RIDGE,bd=1)
		self.resetVisitor()
		self.visitorlogFrm.pack(side = tk. TOP , fill=tk.BOTH, expand = True)
		buttonFrm = myFrm(self,bg=clr1  ,relief=tk.RIDGE,bd=1)
		myBtn(buttonFrm, text= ' Refresh ',bg=clr1, fg=clr3, font=(Font_Name, 15),command= self.Handle_Visitor_count,relief=tk.RIDGE,bd=1,width=30 ).grid(row=0,column=0,padx=2,pady=3)
		myBtn(buttonFrm, text= ' Load More Visitors ',bg=clr1, fg=clr3, font=(Font_Name, 15),command= self.Handle_Visitor_count,relief=tk.RIDGE,bd=1,width=30 ).grid(row=0,column=1,padx=2,pady=3)
		buttonFrm.grid_columnconfigure(0, weight=1, uniform="fred")
		buttonFrm.grid_columnconfigure(1, weight=1, uniform="fred")
		buttonFrm.pack(side = tk. BOTTOM , fill=tk.BOTH, expand = True)


	def resetVisitor(self):
		visitors = DB_H.List_Visitor(5)
		for child in self.visitorlogFrm.winfo_children():
			print('[child destroyed]' , child)
			child.destroy()
		global VisitorsListZoom
		VisitorsListZoom = []
		for visitor in visitors:
			print(visitor)
			VisitorsListZoom.append(visitor[1])
			VisitorDataShowFrame(self.visitorlogFrm,visitor,bg=clr2,relief=tk.SUNKEN,bd=2).pack(side = tk.TOP , fill=tk.X, expand = True)

	def Handle_Visitor_count(self):
		global DB_H,Visitor_Count_Lbl
		ret = DB_H.All_Current_Visitors()
		cnt = len(ret)
		Visitor_Count_Lbl.configure(text=str(cnt))
		print(ret)
		self.resetVisitor()

class VisitorDataShowFrame(tk.Frame):
	def __init__(self,parent,Visitors_data,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		plate = Visitors_data[1]
		Ts = Visitors_data[2]

		img = cv2.imread(visiterFolder+plate+".jpg")
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		# img = Image.open(visiterFolder+plate+".jpg")
		# img = imutils.resize(img, width=128, height=64)
		img = cv2.resize(img, (120,75))
		self.canvas = tk.Canvas(self, width = 120, height = 75)
		self.photo = ImageTk.PhotoImage(image = Image.fromarray(img))
		self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW )
		self.canvas.bind("<Button-1>", self.openZoomWindow)
		self.canvas.pack(side = tk.LEFT)

		Plate_TS = myFrm(self,bg=clr1  )
		mylbl(Plate_TS, text="Plate : ",bg=clr2, fg=clr3, font=(Font_Name, 15),relief=tk.RIDGE,bd=1).grid(row=0,column=0,sticky='nsew',padx=7,pady=7)
		mylbl(Plate_TS, text=plate,bg=clr2, fg=clr3, font=(Font_Name, 15),relief=tk.RIDGE,bd=1).grid(row=0,column=1,sticky='nsew',padx=7,pady=7)
		mylbl(Plate_TS, text= "Time Stamp : ",bg=clr2, fg=clr3, font=(Font_Name, 15),relief=tk.RIDGE,bd=1).grid(row=1,column=0,sticky='nsew',padx=7,pady=7)
		mylbl(Plate_TS, text= Ts,bg=clr2, fg=clr3, font=(Font_Name, 15),relief=tk.RIDGE,bd=1).grid(row=1,column=1,sticky='nsew',padx=7,pady=7)
		Plate_TS.grid_columnconfigure(0, weight=1, uniform="fred")
		Plate_TS.grid_columnconfigure(1, weight=1, uniform="fred")
		Plate_TS.pack(side = tk.RIGHT , fill=tk.BOTH, expand = True)

	def openZoomWindow(self,event):
		newWindow = ZoomWindow(root,bg=clr2) 


class APIresDataShowFrame(tk.Frame):
	def __init__(self,parent,Visitors_data,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		plate = Visitors_data[1]
		Ts = Visitors_data[2]
		img = cv2.imread(visiterFolder+plate+".jpg")
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		# img = Image.open(visiterFolder+plate+".jpg")
		# img = imutils.resize(img, width=128, height=64)
		img = cv2.resize(img, (120,75))
		self.canvas = tk.Canvas(self, width = 120, height = 75)
		self.photo = ImageTk.PhotoImage(image = Image.fromarray(img))
		self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW )
		# self.canvas.bind("<Button-1>", self.openZoomWindow)
		self.canvas.pack(side = tk.LEFT)

		Plate_TS = myFrm(self,bg=clr1  )
		mylbl(Plate_TS, text="Plate : ",bg=clr2, fg=clr3, font=(Font_Name, 15),relief=tk.RIDGE,bd=1).grid(row=0,column=0,sticky='nsew',padx=7,pady=5)
		mylbl(Plate_TS, text=plate,bg=clr2, fg=clr3, font=(Font_Name, 15),relief=tk.RIDGE,bd=1).grid(row=0,column=1,sticky='nsew',padx=7,pady=5)
		mylbl(Plate_TS, text= "Time Stamp : ",bg=clr2, fg=clr3, font=(Font_Name, 15),relief=tk.RIDGE,bd=1).grid(row=1,column=0,sticky='nsew',padx=7,pady=5)
		mylbl(Plate_TS, text= Ts,bg=clr2, fg=clr3, font=(Font_Name, 15),relief=tk.RIDGE,bd=1).grid(row=1,column=1,sticky='nsew',padx=7,pady=5)
		Plate_TS.grid_columnconfigure(0, weight=1, uniform="fred")
		Plate_TS.grid_columnconfigure(1, weight=1, uniform="fred")
		Plate_TS.pack(side = tk.RIGHT , fill=tk.BOTH, expand = True)




class BottomFrame(tk.Frame):
	def __init__(self,parent,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		Heading = 'This Is Status...'
		global Status_Lbl 
		Status_Lbl =  mylbl(self, text= Heading,bg=clr1, fg=clr3, font=(Font_Name, 10),relief=tk.RIDGE,bd=3)
		Status_Lbl.pack(fill=tk.X)

class ZoomWindow(tk.Toplevel):
	def __init__(self,parent,*args,**kwargs):
		tk.Toplevel.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		self.title("New Window")
		self.geometry("800x600") 
		global VisitorsListZoom
		self.index = 0
		plate = VisitorsListZoom[0]
		img = cv2.imread(visiterFolder+plate+".jpg")
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = cv2.resize(img, (700,500))
		self.canvas = tk.Canvas(self, width = 700, height = 500)
		self.photo = ImageTk.PhotoImage(image = Image.fromarray(img))
		self.imgOnCanvas = self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW )
		self.canvas.pack(side = tk.TOP)

		buttonFrm = myFrm(self,bg=clr1  ,relief=tk.RIDGE,bd=1)
		myBtn(buttonFrm, text= ' ---> ',bg=clr1, fg=clr3, font=(Font_Name, 25),command= self.RotateR,relief=tk.RIDGE,bd=1,width=30 ).grid(row=0,column=2,padx=7,pady=7)
		self.lbl = mylbl(buttonFrm, text= '1/5',bg=clr1, fg=clr3, font=(Font_Name, 25),relief=tk.RIDGE,bd=1,width=30 )
		self.lbl.grid(row=0,column=1,padx=7,pady=7)
		myBtn(buttonFrm, text= ' <--- ',bg=clr1, fg=clr3, font=(Font_Name, 25),command= self.RotateL,relief=tk.RIDGE,bd=1,width=30 ).grid(row=0,column=0,padx=7,pady=7)
		
		self.lbl1 = mylbl(buttonFrm, text= plate,bg=clr1, fg=clr3, font=(Font_Name, 15),relief=tk.RIDGE,bd=1,width=30 )
		self.lbl1.grid(row=1,column=0,padx=7,pady=7,columnspan=3)

		buttonFrm.grid_columnconfigure(0, weight=1, uniform="fred")
		buttonFrm.grid_columnconfigure(1, weight=1, uniform="fred")
		buttonFrm.grid_columnconfigure(2, weight=1, uniform="fred")
		buttonFrm.pack(side = tk. BOTTOM , fill=tk.BOTH, expand = True)

	def RotateR(self):
		print('RotateR')
		self.index = (self.index+1)%5
		plate = VisitorsListZoom[self.index]
		print(plate,self.index)
		img = cv2.imread(visiterFolder+plate+".jpg")
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.lbl.configure(text=str(self.index+1)+'/5')
		self.lbl1.configure(text=str(plate))
		img = cv2.resize(img, (600,500))		
		self.photo = ImageTk.PhotoImage(image = Image.fromarray(img))
		# self.canvas.create_image(0, 0, image = photo, anchor = tk.NW)	
		self.canvas.itemconfig(self.imgOnCanvas ,image = self.photo, anchor = tk.NW)	


	def RotateL(self):
		print('RotateL')
		self.index = (self.index-1)%5
		plate = VisitorsListZoom[self.index]
		img = cv2.imread(visiterFolder+plate+".jpg")
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.lbl.configure(text=str(self.index+1)+'/5')
		self.lbl1.configure(text=str(plate))
		img = cv2.resize(img, (600,500))		
		self.photo = ImageTk.PhotoImage(image = Image.fromarray(img))
		# self.canvas.create_image(0, 0, image = photo, anchor = tk.NW)
		self.canvas.itemconfig(self.imgOnCanvas  ,image = self.photo, anchor = tk.NW)	

class EditLinesWindow(tk.Toplevel):
	def __init__(self,parent,*args,**kwargs):
		tk.Toplevel.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		self.title("New Window")
		self.geometry("800x600") 
		tk.Label(self,text ="Line Adjustment Window",bg=clr1,fg= clr3,font=(Font_Name, 25),relief=tk.RIDGE,bd=1).pack(side=tk.TOP , fill = tk.X) 
		
		radioBtnFrame = tk.Frame(self,bg=clr1)
		self.var = tk.IntVar()
		R1 = tk.Radiobutton(radioBtnFrame, text="Up_Limit",     bg=clr2,fg=clr3 , variable=self.var, value=1,command=self.sel)
		R1.pack( side = tk.LEFT, fill = tk.X , expand = True)
		R2 = tk.Radiobutton(radioBtnFrame, text="Down_Limit",   bg=clr2,fg=clr3 , variable=self.var, value=2,command=self.sel)
		R2.pack( side = tk.LEFT, fill = tk.X , expand = True)
		R3 = tk.Radiobutton(radioBtnFrame, text="Line_Up1",     bg=clr2,fg=clr3 , variable=self.var, value=3,command=self.sel)
		R3.pack( side = tk.LEFT, fill = tk.X , expand = True)
		R4 = tk.Radiobutton(radioBtnFrame, text="Line_Up2",     bg=clr2,fg=clr3 , variable=self.var, value=4,command=self.sel)
		R4.pack( side = tk.LEFT, fill = tk.X , expand = True)
		R5 = tk.Radiobutton(radioBtnFrame, text="Line_Down1",   bg=clr2,fg=clr3 , variable=self.var, value=5,command=self.sel)
		R5.pack( side = tk.LEFT, fill = tk.X , expand = True)
		R6 = tk.Radiobutton(radioBtnFrame, text="Line_Down2",   bg=clr2,fg=clr3 , variable=self.var, value=6,command=self.sel)
		R6.pack( side = tk.LEFT, fill = tk.X , expand = True)
		btn = tk.Button(radioBtnFrame,  font=(Font_Name, 15), bg=clr2,fg=clr3 , text =" SAVE ",  command = self.SAVEandCLOSE) 
		btn.pack(side = tk.LEFT, fill = tk.X , expand = True)
		radioBtnFrame.pack(side = tk.TOP , fill = tk.X , expand = True)

		self.VidPara = (800,600)
		self.canvas = tk.Canvas(self, bg = clr2,width = self.VidPara[0], height = self.VidPara[1])
		# self.canvas = tk.Canvas(self, width = self.VidPara[0], height = self.VidPara[1])
		self.canvas.pack()
		global Frame_1
		Frame_1 = cv2.cvtColor(Frame_1, cv2.COLOR_BGR2RGB)
		self.H,self.W,_=Frame_1.shape
		Frame_1 = imutils.resize(Frame_1, width=self.VidPara[0], height=self.VidPara[1])

		self.drawLines(Frame_1.copy())
		self.canvas.bind("<Button-1>", self.callback)

		global Pause_main
		Pause_main = True
		self.transient(root) #set to be on top of the main window
		self.grab_set() #hijack all commands from the master (clicks on the main window are ignored)
		root.wait_window(self) 
		# self.focus_force()
	
	def callback(self,event):
		global frame1,Up_Limit,Down_Limit,Line_Up1,Line_Down1,Line_Up2,Line_Down2
		print("clicked at", event.x, event.y)
		temp = self.var.get()
		if temp == 1:
			Up_Limit = event.y/600
		elif temp == 2:
			Down_Limit = event.y/600
		elif temp == 3:
			Line_Up1 = event.y/600
		elif temp == 4:
			Line_Up2 = event.y/600
		elif temp == 5:
			Line_Down1 = event.y/600
		elif temp == 6:
			Line_Down2 = event.y/600

		self.drawLines(Frame_1.copy())


	def drawLines(self,f):
		print(Up_Limit,Down_Limit,Line_Up1,Line_Down1,Line_Up2,Line_Down2)

		self.FrameHeight=600
		self.Line_Up1=int(Line_Up1*self.FrameHeight)
		self.Line_Up2=int(Line_Up2*self.FrameHeight)

		self.Line_Down1=int(Line_Down1*self.FrameHeight)
		self.Line_Down2=int(Line_Down2*self.FrameHeight)

		self.Up_Limit=int(Up_Limit*self.FrameHeight)
		self.Down_Limit=int(Down_Limit*self.FrameHeight)

		self.pt1 =  [0, self.Line_Down1]
		self.pt2 =  [self.W, self.Line_Down2]
		self.pts_L1 = np.array([self.pt1,self.pt2], np.int32)
		self.pts_L1 = self.pts_L1.reshape((-1,1,2))

		self.pt3 =  [0, self.Line_Up1]
		self.pt4 =  [self.W, self.Line_Up2]
		self.pts_L2 = np.array([self.pt3,self.pt4], np.int32)
		self.pts_L2 = self.pts_L2.reshape((-1,1,2))

		self.pt5 =  [0, self.Up_Limit]
		self.pt6 =  [self.W, self.Up_Limit]
		self.pts_L3 = np.array([self.pt5,self.pt6], np.int32)
		self.pts_L3 = self.pts_L3.reshape((-1,1,2))

		self.pt7 =  [0, self.Down_Limit]
		self.pt8 =  [self.W, self.Down_Limit]
		self.pts_L4 = np.array([self.pt7,self.pt8], np.int32)
		self.pts_L4 = self.pts_L4.reshape((-1,1,2))

		f=cv2.polylines(f,[self.pts_L1],False,(255,0,0),thickness=5)
		f=cv2.polylines(f,[self.pts_L2],False,(0,0,255),thickness=5)
		f=cv2.polylines(f,[self.pts_L3],False,(255,255,255),thickness=5)
		f=cv2.polylines(f,[self.pts_L4],False,(255,255,255),thickness=5)
		self.photo = ImageTk.PhotoImage(image = Image.fromarray(f))
		self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)



	def sel(self):
		selection = "You selected the option " + str(self.var.get())
		# label.config(text = selection)
	
	def SAVEandCLOSE(self):
		print('New Win Closed')
		global Pause_main
		Pause_main = False
		coord_dict = {
					"Line_Up1":Line_Up1,
					"Line_Up2":Line_Up2,
					"Line_Down1":Line_Down1,
					"Line_Down2":Line_Down2,
					"Up_Limit":Up_Limit,
					"Down_Limit":Down_Limit
					}
		coord_dict = json.dumps(coord_dict, indent = 4)
		print(coord_dict)
		with open("Frame_coord.json", "w") as outfile: 
			outfile.write(coord_dict)
		global detector
		detector.reset_Lines()
		print('calling read lines')
		self.destroy()



class VideoFrame(tk.Label):
	def __init__(self,parent,*args,**kwargs):   
		tk.Label.__init__(self,parent,*args,**kwargs)
		self.parent = parent
		video_source = Video_Path
		self.video_source = video_source
		global Video_Capture
		Video_Capture = MyVideoCapture(self.video_source)
		self.VidPara = (300,400)
		self.canvas = tk.Canvas(self, width = 600, height = 400)
		# self.canvas = tk.Canvas(self, width = self.VidPara[0], height = self.VidPara[1])
		self.canvas.pack()
		self.delay = 15
		global detector
		self.detector = detector
		self.times = []
		self.update()

	def update(self):
		t1  = time.time()
		global Pause_main
		ret, self.frame = Video_Capture.get_frame()
		if ret:
			global Frame_fullRes
			Frame_fullRes = self.frame.copy()
			Frame_fullRes = cv2.cvtColor(Frame_fullRes, cv2.COLOR_BGR2RGB)
			self.frame = imutils.resize(self.frame, width=400, height=300)
			self.ProcessVideo()
			self.frame = imutils.resize(self.frame, width=600, height=400)
			self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.frame))
			self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
		t2 = time.time()                
		self.times.append(t2-t1)
		self.times = self.times[-20:]
		ms = sum(self.times)/len(self.times)*1000
		fps = 1000 / ms
		global Status_Lbl
		try:
			Status_Lbl.configure(text=str(fps))
		except Exception as e:
			print(e)

		self.parent.after(self.delay, self.update)

	def ProcessVideo(self):
		self.frame = self.detector.process_frame(self.frame)
		# self.frame = self.detector.process_frame_fgbg(self.frame)

	
class myBtn(tk.Button):
	def __init__(self,parent,*args,**kwargs):
		tk.Button.__init__(self,parent,*args,**kwargs)
		self.parent = parent

class mylbl(tk.Label):
	def __init__(self,parent,*args,**kwargs):
		tk.Label.__init__(self,parent,*args,**kwargs)
		self.parent = parent

class myFrm(tk.Frame):
	def __init__(self,parent,*args,**kwargs):
		tk.Frame.__init__(self,parent,*args,**kwargs)
		self.parent = parent

class MyVideoCapture:
	def __init__(self, video_source=0):
		# Open the video source
		self.vid = cv2.VideoCapture(video_source)
		# start_frame_number = 500
		# self.vid.set(cv2.CAP_PROP_POS_FRAMES, start_frame_number)
		if not self.vid.isOpened():
			raise ValueError("Unable to open video source", video_source)
		# Get video source width and height
		self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
		self.frame_count = 0
	def reload_video(self , video_source):
		self.vid = cv2.VideoCapture(video_source)
		self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
		self.frame_count = 0

	def get_frame(self):
		global Frame_1
		
		self.frame_count += 1


		if self.vid.isOpened():
			ret=True
			# frame = np.array(ImageGrab.grab(bbox=(80,80,480,380)))

			ret, frame = self.vid.read()
			if self.frame_count == 1:
				Frame_1 = frame
			ret, frame = self.vid.read()

			# ret, frame = self.vid.read()
			# ret, frame = self.vid.read()
			if ret:
				return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
			else:
				return (ret, None)
		else:
			return (ret, None)

	# Release the video source when the object is destroyed
	def __del__(self):
		if self.vid.isOpened():
			self.vid.release()


class Detector():
	def __init__(self):
		self.confThreshold = 0.5  #Confidence threshold
		self.nmsThreshold = 0.4  #Non-maximum suppression threshold
		self.inpWidth = 416 
		self.inpHeight = 416
		self.classes = None
		self.counter = 0
		
		# self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		# 	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		# 	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		# 	"sofa", "train", "tvmonitor"]

		self.CLASSES = ["background", "car","motorbike","bus"]
		self.conf = conf.Conf("config.json")
		self.net = cv2.dnn.readNetFromCaffe(self.conf["prototxt_path"],self.conf["model_path"])
		self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
		self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

		# self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
		# self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
		self.countGoingUp=0
		self.countGoingDown=0
		# self.FrameWidth_orignal=int(self.cap.get(3))
		self.FrameWidth=400
		# self.FrameHeight_orignal=int(self.cap.get(4))
		self.FrameHeight=300
		self.FrameArea=self.FrameHeight*self.FrameWidth
		self.areaTH=self.FrameArea/400
		print('Width x Height',self.FrameWidth,self.FrameHeight)

		self.Line_Up1=int(Line_Up1*self.FrameHeight)
		self.Line_Up2=int(Line_Up2*self.FrameHeight)

		self.Line_Down1=int(Line_Down1*self.FrameHeight)
		self.Line_Down2=int(Line_Down2*self.FrameHeight)

		self.Up_Limit=int(Up_Limit*self.FrameHeight)
		self.Down_Limit=int(Down_Limit*self.FrameHeight)

		self.Line_Down_color=(255,0,0)
		self.Line_Up_color=(0,0,255)
		#       x1    y1
		self.pt1 =  [0, self.Line_Down1]
		#          x2           y2
		self.pt2 =  [self.FrameWidth, self.Line_Down2]
		self.pts_L1 = np.array([self.pt1,self.pt2], np.int32)
		self.pts_L1 = self.pts_L1.reshape((-1,1,2))

		self.Line_Down_slope = ((self.pt2[1]-self.pt1[1])/(self.pt2[0]-self.pt1[0]))
		print('Slope : ',self.Line_Down_slope)

		# y = m*x + c
		# c = y - (m * x)
		self.Line_down_intercept = self.pt1[1] - (self.Line_Down_slope * self.pt1[0])
		print(self.Line_down_intercept)

		self.pt3 =  [0, self.Line_Up1]
		self.pt4 =  [self.FrameWidth, self.Line_Up2]
		self.pts_L2 = np.array([self.pt3,self.pt4], np.int32)
		self.pts_L2 = self.pts_L2.reshape((-1,1,2))

		self.Line_Up_slope = ((self.pt4[1]-self.pt3[1])/(self.pt4[0]-self.pt3[0]))
		print('Slope : ',self.Line_Up_slope)

		# y = m*x + c
		# c = y - (m * x)
		self.Line_up_intercept = self.pt3[1] - (self.Line_Up_slope * self.pt3[0])
		print(self.Line_up_intercept)


		self.pt5 =  [0, self.Up_Limit]
		self.pt6 =  [self.FrameWidth, self.Up_Limit]
		self.pts_L3 = np.array([self.pt5,self.pt6], np.int32)
		self.pts_L3 = self.pts_L3.reshape((-1,1,2))

		self.pt7 =  [0, self.Down_Limit]
		self.pt8 =  [self.FrameWidth, self.Down_Limit]
		self.pts_L4 = np.array([self.pt7,self.pt8], np.int32)
		self.pts_L4 = self.pts_L4.reshape((-1,1,2))

		self.font = cv2.FONT_HERSHEY_SIMPLEX
		self.cars = []
		self.max_p_age = 5
		self.pid = 1        
		self.Log_entry_count = 1

	def reset_Lines(self):
		print("reset_Lines called")
		self.Line_Up1=int(Line_Up1*self.FrameHeight)
		self.Line_Up2=int(Line_Up2*self.FrameHeight)

		self.Line_Down1=int(Line_Down1*self.FrameHeight)
		self.Line_Down2=int(Line_Down2*self.FrameHeight)

		self.Up_Limit=int(Up_Limit*self.FrameHeight)
		self.Down_Limit=int(Down_Limit*self.FrameHeight)

		self.Line_Down_color=(255,0,0)
		self.Line_Up_color=(255,0,255)
		#       x1    y1
		self.pt1 =  [0, self.Line_Down1]
		#          x2           y2
		self.pt2 =  [self.FrameWidth, self.Line_Down2]
		self.pts_L1 = np.array([self.pt1,self.pt2], np.int32)
		self.pts_L1 = self.pts_L1.reshape((-1,1,2))

		self.Line_Down_slope = ((self.pt2[1]-self.pt1[1])/(self.pt2[0]-self.pt1[0]))
		print('Slope : ',self.Line_Down_slope)

		# y = m*x + c
		# c = y - (m * x)
		self.Line_down_intercept = self.pt1[1] - (self.Line_Down_slope * self.pt1[0])
		print(self.Line_down_intercept)

		self.pt3 =  [0, self.Line_Up1]
		self.pt4 =  [self.FrameWidth, self.Line_Up2]
		self.pts_L2 = np.array([self.pt3,self.pt4], np.int32)
		self.pts_L2 = self.pts_L2.reshape((-1,1,2))

		self.Line_Up_slope = ((self.pt4[1]-self.pt3[1])/(self.pt4[0]-self.pt3[0]))
		print('Slope : ',self.Line_Up_slope)

		# y = m*x + c
		# c = y - (m * x)
		self.Line_up_intercept = self.pt3[1] - (self.Line_Up_slope * self.pt3[0])
		print(self.Line_up_intercept)

		self.pt5 =  [0, self.Up_Limit]
		self.pt6 =  [self.FrameWidth, self.Up_Limit]
		self.pts_L3 = np.array([self.pt5,self.pt6], np.int32)
		self.pts_L3 = self.pts_L3.reshape((-1,1,2))

		self.pt7 =  [0, self.Down_Limit]
		self.pt8 =  [self.FrameWidth, self.Down_Limit]
		self.pts_L4 = np.array([self.pt7,self.pt8], np.int32)
		self.pts_L4 = self.pts_L4.reshape((-1,1,2))

	def process_frame(self,frame):
		self.frame = frame
		self.counter+=1
		# Create a 4D blob from a frame.
		self.blob = cv2.dnn.blobFromImage(self.frame, size=(300, 300),ddepth=cv2.CV_8U)
		self.net.setInput(self.blob, scalefactor=1.0/127.5, mean=[127.5,127.5, 127.5])
		self.detections = self.net.forward()

		for i in self.cars:
			i.age_one()
		
		for i in np.arange(0, self.detections.shape[2]):
			# extract the confidence (i.e., probability) associated
			# with the prediction
			self.confidence = self.detections[0, 0, i, 2]

			# filter out weak detections by ensuring the `confidence`
			# is greater than the minimum confidence
			if self.confidence > self.conf["confidence"]:
				# extract the index of the class label from the
				# detections list
				self.idx = int(self.detections[0, 0, i, 1])

				# if the class label is not a car, ignore it
				if self.CLASSES[self.idx] not in[ "car" , "bicycle" , "motorbike" , "bus"]:
					continue

				# compute the (x, y)-coordinates of the bounding box
				# for the object
				(self.H, self.W) = self.frame.shape[:2]

				self.box = self.detections[0, 0, i, 3:7] * np.array([self.W, self.H, self.W, self.H])
				(self.startX, self.startY, self.endX, self.endY) = self.box.astype("int")

				cv2.rectangle(self.frame, (self.startX, self.startY), (self.endX, self.endY), (255, 197, 74), 3)

				self.Box_w     = self.endX-self.startX
				self.Box_h     = self.endY-self.startY
				self.Box_cen_x = (self.endX-self.startX)//2
				self.Box_cen_y = (self.endY-self.startY)//2
				if self.area(self.Box_w , self.Box_h)>self.areaTH:
					self.cx = self.startX+int(self.Box_w//2)
					self.cy = self.startY+int(self.Box_h)
					self.x,self.y,self.w,self.h=self.startX,self.startY,self.Box_w,self.Box_h
					self.new=True
					if self.cy in range(self.Up_Limit,self.Down_Limit):
						for i in self.cars:
							if abs(self.cx - i.getX()) <= self.w and abs(self.cy - i.getY()) <= self.h:
								self.new = False
								i.updateCoords(self.cx, self.cy)
								self.y_limit_up = int(self.Line_Up_slope*self.cx + self.Line_up_intercept)
								self.y_limit_down = int(self.Line_Down_slope*self.cx + self.Line_down_intercept)
								# cv2.line(self.frame, (self.cx, self.cy), (self.cx, self.y_limit_down), (0, 255, 0), 3)
								global Up_Count_Lbl , Down_Count_Lbl
								timestamp = int(time.time())
								dt_object = datetime.fromtimestamp(timestamp)
								Ts = str(dt_object)

								if i.going_UP(self.y_limit_up,self.y_limit_up)==True:
									self.countGoingUp+=1
									Up_Count_Lbl.configure(text=str(self.countGoingUp))
									flag_detected = True
									print(self.CLASSES[self.idx] , "ID:", i.getId(), 'crossed going up at', time.strftime("%c"))
									
									self.Log_entry_count += 1
									mylbl(Log_Canvas, text= self.CLASSES[self.idx], bg=clr2, fg=clr3, font=(Font_Name, 10)).grid(row=self.Log_entry_count,column=0)
									mylbl(Log_Canvas, text= i.getId(),              bg=clr2, fg=clr3, font=(Font_Name, 10)).grid(row=self.Log_entry_count,column=1)
									mylbl(Log_Canvas, text= 'OUT',                  bg=clr2, fg=clr3, font=(Font_Name, 10)).grid(row=self.Log_entry_count,column=2)
									mylbl(Log_Canvas, text= time.strftime("%c"),    bg=clr2, fg=clr3, font=(Font_Name, 10)).grid(row=self.Log_entry_count,column=3)
									
									self.H,self.W,_ = self.frame.shape
									self.H1,self.W1,_ = Frame_fullRes.shape
									self.xx = ((self.W1*self.x)//self.W)
									self.xxe = ((self.W1*self.endX)//self.W)
									self.yy = ((self.H1*self.y)//self.H)
									self.yye = ((self.H1*self.endY)//self.H)
									tempTh = threading.Thread(target=ApiCallFunc  , args=[self.xx, self.xxe, self.yy, self.yye, Frame_fullRes.copy(),Ts,"OUT"])
									Que.put(tempTh)
								
								elif i.going_DOWN(self.y_limit_down,self.y_limit_down)==True:
									print(self.CLASSES[self.idx] , "ID:", i.getId(), 'crossed going Down at', time.strftime("%c"))

									self.countGoingDown+=1
									Down_Count_Lbl.configure(text=str(self.countGoingDown))
									flag_detected = True
									self.Log_entry_count += 1
									mylbl(Log_Canvas, text= self.CLASSES[self.idx], bg=clr2, fg=clr3, font=(Font_Name, 10)).grid(row=self.Log_entry_count,column=0)
									mylbl(Log_Canvas, text= i.getId(),              bg=clr2, fg=clr3, font=(Font_Name, 10)).grid(row=self.Log_entry_count,column=1)
									mylbl(Log_Canvas, text= 'IN',                   bg=clr2, fg=clr3, font=(Font_Name, 10)).grid(row=self.Log_entry_count,column=2)
									mylbl(Log_Canvas, text= time.strftime("%c"),    bg=clr2, fg=clr3, font=(Font_Name, 10)).grid(row=self.Log_entry_count,column=3)

									self.H,self.W,_ = self.frame.shape
									self.H1,self.W1,_ = Frame_fullRes.shape
									self.xx = ((self.W1*self.x)//self.W)
									self.xxe = ((self.W1*self.endX)//self.W)
									self.yy = ((self.H1*self.y)//self.H)
									self.yye = ((self.H1*self.endY)//self.H)
									tempTh = threading.Thread(target=ApiCallFunc  , args=[self.xx, self.xxe, self.yy, self.yye, Frame_fullRes.copy(),Ts,"IN"])
									Que.put(tempTh)
								break

						for i in self.cars:
							if i.getState()=='1':
								if i.getDir()=='down' and i.getY()>self.Down_Limit:
									i.setDone()
								elif i.getDir()=='up' and i.getY()<self.Up_Limit:
									i.setDone()
							if i.timedOut():
								self.index=self.cars.index(i)
								print('[ car len ]' , len(self.cars))
								self.cars.pop(self.index)
								print('[ car len ]' , len(self.cars))
								del i
								

						if self.new==True: #If nothing is detected,create new
							self.p=vehicles.Car(self.pid,self.cx,self.cy,self.max_p_age)
							self.cars.append(self.p)
							self.pid+=1
							print('new car with',self.pid)
							
					cv2.rectangle(self.frame,(self.x,self.y),(self.x+self.w,self.y+self.h),(0,0,0),2)

			for i in self.cars:
				cv2.circle(self.frame,(i.getX(),i.getY()),9,(0,0,0),-1)
				cv2.circle(self.frame,(i.getX(),i.getY()),7,i.getRGB(),-1)
				cv2.putText(self.frame, str(i.getId()), (i.getX()-5, i.getY()+3), self.font, 0.3, (0,0,0), 1, cv2.LINE_AA)

				# cv.circle(self.frame,(self.cx,self.cy),5,(255,255,255),-1)

		self.str_up='UP: '+str(self.countGoingUp)
		self.str_down='DOWN: '+str(self.countGoingDown)
		self.frame=cv2.polylines(self.frame,[self.pts_L1],False,(0,0,0),thickness=3)
		self.frame=cv2.polylines(self.frame,[self.pts_L1],False,self.Line_Down_color,thickness=1)
		self.frame=cv2.polylines(self.frame,[self.pts_L2],False,(0,0,0),thickness=3	)
		self.frame=cv2.polylines(self.frame,[self.pts_L2],False,self.Line_Up_color,thickness=1)
		self.frame=cv2.polylines(self.frame,[self.pts_L3],False,(0,0,0),thickness=2)
		self.frame=cv2.polylines(self.frame,[self.pts_L3],False,(255,255,255),thickness=1)
		self.frame=cv2.polylines(self.frame,[self.pts_L4],False,(0,0,0),thickness=2)
		self.frame=cv2.polylines(self.frame,[self.pts_L4],False,(255,255,255),thickness=1)
		# cv2.putText(self.frame, self.str_up, (10, 40), self.font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
		# cv2.putText(self.frame, self.str_up, (10, 40), self.font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
		# cv2.putText(self.frame, self.str_down, (10, 90), self.font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
		# cv2.putText(self.frame, self.str_down, (10, 90), self.font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
		return self.frame

	def area(self,w,h):
		return w*h


def HendleQueue(q):
	while True:
		print("############################# Size ############################", q.qsize())
		if q.qsize() > 0:
			print('if')
			x = q.get()
			print(x)
			x.start()
			x.join()
		else:
			time.sleep(3)
		global RECORDS_FOR_DB ,TimeCounter
		if TimeCounter == 0:
			TimeCounter = time.time()
		elif time.time() - TimeCounter >= 20:
			TimeCounter = time.time()
			print(' [ 1 Min Pass ] ')
			DB_H.LogDB(RECORDS_FOR_DB)
			RECORDS_FOR_DB = []


Api_count = 0
TimeCounter = 0
RECORDS_FOR_DB = []

def ApiCallFunc(xx,xxe,yy,yye,frame1,Ts,DIR):
	print("================== Req Sent {} ====================".format(Api_count))
	TempImg = frame1[yy:yye , xx:xxe]
	cv2.imwrite(r'test.jpg' , TempImg)
	with open(r"test.jpg", 'rb') as fp:
		response = requests.post(
			'http://192.168.1.223:8000/test/',
			files=dict(Img_upload=fp))
	print("================== Res Get ====================")
	pprint(response.json())
	val = dict()
	try:
		pass    
		dix = json.loads((str(response.content)[2:-1]))
		print(dix)
		dix = dict(dix)
		detected = dix['Key']['No_Plate']
		if detected:
			AllKeys = list(dix['Key']['Detecte_Plates'].keys())
			print(AllKeys)
			for i,key in enumerate(AllKeys):
				print('[KEY]',key)
				plateFound = dix['Key']['Detecte_Plates'][key]['FINAL_PRED']['Result']
				# TempImg = cv2.resize(TempImg,(128,128))
				# print('[IMG WRITE]',visiterFolder+plateFound+'.jpg')
				if len(plateFound)>8:
					cv2.imwrite(visiterFolder+plateFound+'.jpg',TempImg)
					RECORDS_FOR_DB.append((Ts,plateFound,DIR))
					data = ((1,plateFound,Ts))
					# print('X*X*'*100)
					global Api_Res_Frm
					# APIresDataShowFrame(Api_Res_Frm,data,bg=clr2,relief=tk.SUNKEN,bd=2).pack(side = tk.TOP , fill=tk.X, expand = True)


					#APIresDataShowFrame
		print(' [ RECORDS_FOR_DB ]' , RECORDS_FOR_DB)

	except Exception as e:
		print(e)
		val={'error':e}

def main():
	global Que,DB_H,MailOBJ
	Que =  queue.Queue()
	print('[DB REQ SENT]')
	DB_H = DB.DB_Handle()
	MailOBJ = Email.alert_Handle(DB_H.db)
	print(DB_H)
	# print(dir(q))
	# mainTh = threading.Thread(target=detector.start , args=[q] )
	funTh = threading.Thread(target=HendleQueue , args=[Que])
	# mainTh.start()
	funTh.start()
	global detector
	detector = Detector()

	global root
	root = tk.Tk()
	root.geometry('1366x768')
	root.title('SIH2020')
	root.configure(background=clr1)
	menubar = MenuBar(root)
	root.config(menu=menubar)
	MainApp(root).pack(side = tk.TOP,fill = tk.BOTH,expand=True)

	root.mainloop()

if __name__ == '__main__':
	main()
