from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

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
    location = models.CharField(max_length=50,blank=True,null = True)

    def __str__(self):
        return self.user.username

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='customer')
    avatar = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 128, blank = True)
    address = models.CharField(max_length = 128, blank = True)

    def __str__(self):
        return self.user.username

class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    image = models.ImageField(upload_to='restaurant/meals/')
    price = models.FloatField()

    def __str__(self):
        return self.name

class Order(models.Model):
    COOKING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4

    STATUS_CHOICES = (
        (COOKING , "Cooking"),
        (READY , "Ready"),
        (ONTHEWAY , "On the way"),
        (DELIVERED, "Delivered")
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete = models.CASCADE, blank=True,null=True)
    address = models.CharField(max_length=40)
    total = models.FloatField()
    status = models.IntegerField(choices = STATUS_CHOICES)
    created_at = models.DateTimeField(default = timezone.now)
    picked_up = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.customer.user.username

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.FloatField()
    sub_total = models.FloatField()

    def __str__(self):
        return self.order.customer.user.username

