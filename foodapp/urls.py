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

from .views import (       
    HomeView,
    RestaurantSignupView,
    OrderView,
    MealView,
    AccountView,
    ReportView,
    MySignupView
)

app_name = 'foodapp'
urlpatterns = [ 
    path('', HomeView, name = 'home'),
    path('restaurant-sign-up/', RestaurantSignupView.as_view(), name = 'restaurant-sign-up'),
    path('restaurant/account/order/', OrderView.as_view(), name = 'restaurant-order'),
    path('restaurant/account/meal', MealView.as_view(), name = 'restaurant-meal'),
    path('restaurant/account/', AccountView.as_view(), name = 'restaurant-account'),
    path('restaurant/account/report', ReportView.as_view(), name = 'restaurant-report')
] 