"""foodtasker URL Configuration

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
from django.urls import include
from foodapp.apis import (
    customer_get_restaurant, 
    customer_get_meal,
    customer_get_add_order,
    customer_get_order_latest,
    get_notification, driver_get_order,
    driver_order_pick, driver_order_latest,
    driver_order_complete, driver_order_revenue,
    get_driver_location, driver_location
)
    
from .views import (       
    HomeView,
    RestaurantSignupView,
    OrderView,
    MealView,
    AccountView,
    ReportView,
    MySignupView,
    AddMealView,
    MealEdit
)

app_name = 'foodapp'
urlpatterns = [ 
    path('', HomeView, name = 'home'),
    path('restaurant-sign-up/', RestaurantSignupView.as_view(), name = 'restaurant-sign-up'),
    path('restaurant/account/order/', OrderView.as_view(), name = 'restaurant-order'),
    path('restaurant/account/meal', MealView.as_view(), name = 'restaurant-meal'),
    path('restaurant/account/', AccountView.as_view(), name = 'restaurant-account'),
    path('restaurant/meal/edit/<meal_id>', MealEdit, name = 'restaurant-edit-meal'),
    path('restaurant/account/meal/add', AddMealView.as_view(), name = 'restaurant-add-meal'),
    path('restaurant/account/report', ReportView.as_view(), name = 'restaurant-report'),

    # API FOR CUSTOMERS
    path('api/customer/restaurant', customer_get_restaurant),
    path('api/customer/meals/<meal_id>/', customer_get_meal),
    path('api/customer/order/add/', customer_get_add_order),
    path('api/customer/order/latest/', customer_get_order_latest),
    path('api/customer/order/notification/<last_request_time>/',get_notification),
    path('api/customer/get/driver/location/', get_driver_location),

    # API FOR DRIVERS
    path('api/driver/order/', driver_get_order),
    path('api/driver/order/pick/', driver_order_pick),
    path('api/driver/order/latest/', driver_order_latest),
    path('api/driver/order/complete/', driver_order_complete),
    path('api/driver/order/revenue/', driver_order_revenue),
    path('api/driver/location/', driver_location),



] 