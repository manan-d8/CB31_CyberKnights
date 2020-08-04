# Number Plate Detection Model

## Old Model
### We Used YoloV3 for Number Plate Detection.
### Model is Trained on Approximate 2000 Images.
### Acc : 92.21%
### IOU : 72.89%

## New Model
### We used YoloV3 for Number Plate Detection.
### Model is Trained on Approximate 3700 Images.
### Acc : 93.84%
### IOU : 74.16%

### please Change Weights And Weights path accordingly...

# How To Use ?
##### Step 1 
* Dawnload Our Weights File From [here](https://drive.google.com/file/d/1WNTDGM_KNtGj5SNAcDJ6-hfmxlJB1UAf/view?usp=sharing)
* Put this Weights File in Weights Folder in Noplate_Detection Folder

##### step 2
* Install Python 3.8.0
https://www.python.org/downloads/
* Install numpy
> !pip install numpy
* Install opencv
* for CPU
> !pip install opencv-python

* If you want to use GPU You have to build opencv from source with cuda support which will increase perfomance of the model.

##### step 3
* run Python file 
> !python NoPlateDetector.py

* It will Show results for all imgs available in Test_Images folder.
* And also Write output files in results folder.

# Test Screenshots
![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Noplate_Detection/Results/NoPlateRes7.jpg)

![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Noplate_Detection/Results/NoPlateRes9.jpg)

![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Noplate_Detection/Results/NoPlateRes8.jpg)

![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Noplate_Detection/Results/NoPlateRes6.jpg)


