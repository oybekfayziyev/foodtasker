from django.db import models
from django.conf import settings
# Create your models here.
class Restaurant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    name = models.CharField(max_length = 30)
    phone = models.CharField(max_length = 30)    
    address = models.CharField(max_length = 50)
    logo = models.ImageField(upload_to = 'retaurant/')

    def __str__(self):
        return self.name    