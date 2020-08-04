# Character Recognition Model
## Old Model
### We Used AlexNet with tensorflow / Keras for character Recognition.
### Model is Trained on 36000 Images  with each class having 1000 images.
### Acc : 83.14%

## New Model
### We have ensembled ResNetV2, ResNet, DenseNet169 Models for character Recognition.
### Model is Trained on 36000 Images with each class having 1000 images.
### Acc : 90.1%

### please Change Weights And Weights path accordingly...

# How To Use ?
##### Step 1 
* Download Our Weights File From [here](https://drive.google.com/file/d/1Z5ZFATBNEarQfEa5KhLY1ybzg_TDdko0/view?usp=sharing)
* Put this Weights File in Weights Folder in Character_Segmentation Folder

##### step 2
* Install Python 3.8.0
https://www.python.org/downloads/
* Install numpy
> !pip install numpy
* Install opencv
* for CPU
> !pip install opencv-python
* If you want to use GPU You have to build opencv from source with cuda support which will increase performance of the model.
* Install Tensorflow == 2.0
* for CPU
> !pip install tensorflow
* for GPU
> pip install tensorflow-gpu

##### step 3
* run Python file 
> !python CharRecognition.py

* It will Show results for all imgs available in Test_Images folder.
* And also Write output files in results folder.

# Test Screenshots
![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Character_Recognition/Results/CharReco1.jpg)
![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Character_Recognition/Results/CharReco2.jpg)
![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Character_Recognition/Results/CharReco3.jpg)
![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Character_Recognition/Results/CharReco5.jpg)

![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Character_Recognition/Results/CharReco6.jpg)
![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Character_Recognition/Results/CharReco7.jpg)
![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Character_Recognition/Results/CharReco8.jpg)
![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Seprate_modules/Character_Recognition/Results/CharReco9.jpg)
