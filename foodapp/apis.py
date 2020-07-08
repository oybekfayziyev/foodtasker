from foodapp.models import Restaurant, Order, Meal, OrderDetail
from django.contrib.auth.models import User
from foodapp.serializers import RestaurantSerializer, MealSerializer, OrderSerializer
from django.http import JsonResponse
import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.models import AccessToken

def customer_get_restaurant(request):
   
    restaurant = RestaurantSerializer(instance = Restaurant.objects.all().order_by('-id'),
                                      many=True, context = {'request' : request}).data

    return JsonResponse({'restaurant' : restaurant})

def customer_get_meal(request,meal_id):
    print(Restaurant.objects.filter(id =1))
    meal = MealSerializer(instance = Meal.objects.filter(restaurant_id = meal_id), 
                          many=True, context = {'request' : request}
                          ).data 

    return JsonResponse({'meal' : meal})

@csrf_exempt
def customer_get_add_order(request):    

    if request.method == "POST":
        print("access",request.POST.get('access_token'))
        access_token = AccessToken.objects.get(token = request.POST.get('access_token'), expires__gt = timezone.now())
        print(access_token.user.customer)
        customer = access_token.user.customer

        if Order.objects.filter(customer = customer).exclude(status = Order.DELIVERED):
            return JsonResponse({'status' : 'failed','error':'Order already delivered'})
        
        if not request.POST['address']:
            return JsonResponse({'status':'failed','error':'Include address'})
        
        order_details = json.loads(request.POST['order_details'])
        order_total = 0
        for i in order_details:          
            order_total += Meal.objects.get(id = i['meal_id']).price * i['quantity']
        

        print(Order.objects.all())

        if len(order_details) > 0:
            order = Order.objects.create(
                customer = customer,
                restaurant_id = request.POST['restaurant_id'],                
                total = order_total,
                status = Order.COOKING,
            )
            for meal in order_details:
                OrderDetail.objects.create(
                                            order = order,
                                            meal_id = meal['meal_id'],
                                            quantity=meal['quantity'],
                                            sub_total=Meal.objects.get(id=meal['meal_id']).price * meal['quantity']
                                        )
        
        return JsonResponse({'status':'success'})

def customer_get_order_latest(request):
    access_token = AccessToken.objects.get(token=request.GET.get('access_token'),expires__gt = timezone.now())
    customer = access_token.user.customer
    print('customer',customer)
    order = OrderSerializer(Order.objects.filter(customer=customer).last()).data

    return JsonResponse({'order' : order})

def get_notification(request,last_request_time):
    
    notification = Order.objects.filter(restaurant = request.user.restaurant, created_at__gt=last_request_time).count()

    return JsonResponse({'notification' : notification})

# API FOR DRIVERS
def driver_get_order(request):
    order = OrderSerializer(instance = Order.objects.filter(status = Order.READY, driver = None), many = True).data

    return JsonResponse({'order' : order})

@csrf_exempt
def driver_order_pick(request):

    if request.method == "POST":
        print('token',request.POST['access_token'])
        
        access_token = AccessToken.objects.get(token = request.POST['access_token'], expires__gt=timezone.now())
        driver = access_token.user.driver

        if Order.objects.filter(driver = driver).exclude(status=Order.ONTHEWAY):
            return JsonResponse({'status' : 'failed','error' : 'You can only pick one item at the time'})
        
        try:
            order = Order.objects.get(id = request.POST['order_id'],driver = None, status = Order.READY)
            order.driver = driver
            order.status = Order.ONTHEWAY
            order.picked_up = timezone.now()
            order.save()

            return JsonResponse({"status" : "Success"})
        except:
            return JsonResponse({"status" :"failed",'error' : 'Object does not exist'})

def driver_order_revenue(request):
    access_token = AccessToken.objects.get(token = request.GET['access_token'],expires__gt = timezone.now())
    driver = access_token.user.driver

    from datetime import timedelta
    revanue = {}
    today = timezone.now()
    current_weekdays = [today + timedelta(days=i) for i in range(0-today.weekday(),7-today.weekday())]

    for day in current_weekdays:
        orders = Order.objects.filter(
            driver = driver,
            status = Order.DELIVERED,
            created_at__day = day.day,
            created_at__year = day.year,
            created_at__month = day.month
        )
        revanue[day.strftime("%a")] = sum(order.total for order in orders)
    
    return JsonResponse({"revanue" : revanue})

@csrf_exempt
def driver_order_complete(request):

    access_token = AccessToken.objects.get(token=request.POST['access_token'],expires__gt=timezone.now())
    driver = access_token.user.driver

    order = Order.objects.get(id = request.POST['id'],driver=driver)
    order.status = Order.DELIVERED
    order.save()

    return JsonResponse({"order" : "success"})

def driver_order_latest(request):
    access_token = AccessToken.objects.get(token = request.GET['access_token'],expires__gt=timezone.now())
    driver = access_token.user.driver

    order = OrderSerializer(Order.objects.filter(driver=driver).order_by('picked_up').last()).data

    return JsonResponse({"order" : order})

# GET DRIVER LOCATION
def get_driver_location(request):
    access_token = AccessToken.objects.get(token = request.GET['access_token'], expires__gt=timezone.now())

    customer = access_token.user.customer
    print('customer',customer)
    order = Order.objects.filter(customer=customer,status=Order.ONTHEWAY).last()
    print('order',order)
    location = order.driver.location

    return JsonResponse({"location" : location})

@csrf_exempt
def driver_location(request):
    
    if request.method == "POST":
        access_token = AccessToken.objects.get(token = request.POST['access_token'],expires__gt=timezone.now())
        driver = access_token.user.driver

        driver.location = request.POST['location']
        driver.save()

        return JsonResponse({"location" : driver.location})