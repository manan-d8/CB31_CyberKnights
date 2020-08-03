# How TO Install Server
## step 1
set up enviroment on anaconda with python3.8
and activate the enviroment

## step 2
install dependencies
> !pip install django

> !pip install djangorestframework

> !pip install opencv-python

> !pip install opencv-contrib-python

> !pip install scipy

> !pip install imutils

> !pip install python-docx

> !pip install tensorflow

> !pip install matplotlib


## step 3
download below mentoined weights from drive link: https://drive.google.com/drive/folders/1zP2cQ_LVuVzXykqso9mVDAjvDTHYF4nR?usp=sharing

* DenseNet169_E10.hdf5

* ResNetV2_Epoch_20.hdf5

* ResNet_Epoch_20.hdf5

* YoloV3SIH(NoPlate-Final)_final.weights

* YoloV3SIH(Segmentation)_final.weights

copy all the weights in weights folder

## step 4
use ipconfig to get ip of pc

note: both server and client should be in same folder

use this command to run server on your localhost

> python manage.py runserver <ip of your pc>

note: it will take time to load the first time you run it.


## step 5
open web api in browser

https://<ip of your pc>:8000
