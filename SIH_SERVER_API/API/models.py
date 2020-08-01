from django.db import models

# Create your models here.
class Image_Upload(models.Model): 
	# name = models.CharField(max_length=50)
	Img_upload = models.ImageField(upload_to='images/') 

