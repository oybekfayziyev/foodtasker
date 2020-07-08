from rest_framework import serializers
from foodapp.models import Restaurant, Meal, Order, Driver, Customer, OrderDetail
from django.contrib.auth.models import User

class RestaurantSerializer(serializers.ModelSerializer):
    
    logo = serializers.SerializerMethodField()

    def get_logo(self,restaurant):
        request = self.context.get('request')
       
        logo_url = restaurant.logo.url
        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Restaurant
        fields = ('id','name','address','phone','logo')

class MealSerializer(serializers.ModelSerializer):
  
    image = serializers.SerializerMethodField()

    def get_image(self,meal):
        request = self.context.get('request')
        image_url = meal.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Meal
        fields = ('id','name','description','image','price')

class OrderMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id','name','description','price')


class AddOrderSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Order
        fields = ('__all__')

class AccountSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Restaurant
        fields = ('id','name','address','phone','logo')

class DriverSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source = 'user.get_full_name')
    class Meta:
        model = Driver
        fields = ('id','name','avatar','phone','address')

class OrderCustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source = 'user.get_full_name')
    class Meta:
        model = Customer
        fields = ('id','name','avatar','phone','address')

class OrderDetailSerializer(serializers.ModelSerializer):
    # order = OrderSerializer()
    meal = OrderMealSerializer
    print('meal',meal)
    class Meta:
        model = OrderDetail
        fields = ('id','meal','quantity','sub_total')

class OrderRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id','name','address','phone')

class OrderSerializer(serializers.ModelSerializer):
    customer = OrderCustomerSerializer()
    restaurant = OrderRestaurantSerializer()
    driver = DriverSerializer()
    print(driver)
    order_details = OrderDetailSerializer(many=True)
    status = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = Order
        fields = ('id','customer','restaurant','driver','order_details','total','status','created_at')



