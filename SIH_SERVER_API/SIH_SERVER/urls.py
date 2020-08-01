"""SIH_SERVER URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from API import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index.as_view(), name='index'),
    path('test/', views.test, name='upload'),
    path('login/', views.Login.as_view(), name='login'),
    path('SignUp/', views.SignUp.as_view(), name='SignUp'),
    path('LogOut/', views.LogOut.as_view()),
    path('AccDetails/', views.AccountDetail.as_view(), name = "AccountDetail"),
    path('ApiInfo/', views.ApiInfo.as_view(), name = "ApiInfo"),
    # path('NoPlateResPage/' , views.NoPlateResPage.as_view(),  name='NoPlateResPage'),
    path('success/', views.success, name = 'success'), 
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)