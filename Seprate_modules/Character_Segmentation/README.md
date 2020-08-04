# Charecter Segmentation Model
## Old Model
### We Used YoloV3 for Character Segmentation.
### Model is Trained on Approximate 1000 Images with each having 8-10 charecters.
### Acc : 95.50%
### IOU : 76.64%

## New Model
### We used YoloV3 for Character Segmentation.
### Model is Trained on Approximate 2200 Images with each having 8-10 characters.
### Acc : 97.38%
### IOU : 76.87%

### please Change Weights And Weights path accordingly...

# How To Use ?
##### Step 1 
* Dawnload Our Weights File From [here](https://drive.google.com/file/d/1l3Nr6pL-xk0jxI-HtO2-tgKL5aJLcsLa/view?usp=sharing)
* Put this Weights File in Weights Folder in Character_Segmentation Folder

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
> !CharsSegment.py

* It will Show results for all imgs available in Test_Images folder.
* And also Write output files in results folder.

# Test Screenshots
![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Character_Segmentation/Results/CharSeg9.jpg)

![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Character_Segmentation/Results/CharSeg6.jpg)

![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Character_Segmentation/Results/CharSeg1.jpg)

![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Character_Segmentation/Results/CharSeg2.jpg)

![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Character_Segmentation/Results/CharSeg5.jpg)
