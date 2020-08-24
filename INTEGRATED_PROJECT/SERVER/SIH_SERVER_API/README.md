# How TO Install Server
## step 1
#### install anaconda on server machine.
set up enviroment on anaconda with python3.8
and activate the enviroment
```
!conda create -n myenv python=3.8 
!conda activate myenv
```
refer : [https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html]


## step 2
install dependencies
```
!pip install django

!pip install djangorestframework

!pip install opencv-python

!pip install opencv-contrib-python

!pip install scipy

!pip install imutils

!pip install python-docx

!pip install tensorflow

!pip install matplotlib
```

## step 3
#### download below mentoined weights from drive link: https://drive.google.com/drive/folders/1zP2cQ_LVuVzXykqso9mVDAjvDTHYF4nR?usp=sharing

* DenseNet169_E10.hdf5

* ResNetV2_Epoch_20.hdf5

* ResNet_Epoch_20.hdf5

* YoloV3SIH(NoPlate-Final)_final.weights

* YoloV3SIH(Segmentation)_final.weights

copy all the weights in weights folder

## step 4
* use ipconfig to get ip of pc
* add your Local Ip in allowed Host List in SIH_SERVER > settings.py 
```
ALLOWED_HOSTS = ['localhost', '127.0.0.1', <YOUR IP> ]
```
##### note: both server and client should be in same Network

* use this command to run server on your localhost
```
python manage.py runserver <YOUR IP>:8000
EX : python manage.py runserver 192.186.1.227:8000
```
### note: it will take time to load When first time you Call Api.

