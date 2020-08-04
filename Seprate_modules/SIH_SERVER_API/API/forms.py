from django import forms 
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ImageUploadForm(forms.ModelForm): 
	class Meta: 
		model = Image_Upload 
		fields = ['Img_upload']
	def __init__(self, *args, **kwargs):
		super(ImageUploadForm, self).__init__(*args, **kwargs)
		self.fields['Img_upload'].widget.attrs['width'] = '90%'

	# def display_NoPlate_images(request): 
	# 	if request.method == 'GET': 
	# 		# getting all the objects of hotel. 
	# 		Hotels = Hotel.objects.all()  
	# 		return render((request, 'NoPlateDisplay.html', 
	# 					 {'hotel_images' : Hotels})) 

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
		self.fields['email'].widget.attrs['placeholder'] = 'Email - Id'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'