# Vehicle Detection

we have used caffe with ssd to train model for vehicle detection

## Training Dataset

we trained on 5000 labelled images for over 15000 iterations
note:stopped at 15000 as loss or accuracy was not improving
evaluation table:
11000 iteration gives 97.5% accuracy on test dataset of 120 images


## How to use
### step 1:
Download latest iteration weights File From the drive link provided in main README file
note: weight should be in same directory as the python file

### step 2
install libraries if not installed:
os, glob, opencv as cv, numpy as np

### step 3
configure config.json, change the .prototxt and .caffemodel file according to the downloaded weight

### step 5
testing images should be stored in Test_images

### step 6
run the caffe_detection.py
```python
!python caffe_detection.py
```

## Results
result of detected vehicles in images will be marked and saved in the Results directory

## Test Screenshots
![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Vehicle%20Detection/Results/1.jpg)

![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Vehicle%20Detection/Results/2.jpg)

![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Vehicle%20Detection/Results/3.jpg)

![Screen Shot 1](https://github.com/manan-d8/CB31_CyberKnights/blob/master/Vehicle%20Detection/Results/4.jpg)
