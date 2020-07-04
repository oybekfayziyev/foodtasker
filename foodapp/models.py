from django.db import models
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    username = models.CharField(max_length = 30)
    email = models.EmailField()
    address = models.CharField(max_length = 30)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 40)
    photo = models.ImageField(upload_to = 'profile/')
    phone = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.user.username

class Restaurant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,related_name ='restaurant')
    name = models.CharField(max_length = 30)
    phone = models.CharField(max_length = 30)    
    address = models.CharField(max_length = 50)
    logo = models.ImageField(upload_to = 'retaurant/')

    def __str__(self):
        return self.name    

class Driver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='driver')
    avatar = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 128, blank = True)
    address = models.CharField(max_length = 128, blank = True)

    def __str__(self):
        return self.user.username

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='customer')
    avatar = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 128, blank = True)
    address = models.CharField(max_length = 128, blank = True)

    def __str__(self):
        return self.user.username