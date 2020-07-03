from django.shortcuts import render, redirect
from django.http import HttpResponse
from allauth.account.views import SignupView
from .forms import SignupForm, RestaurantForm
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Restaurant

# Create your views here.

def HomeView(request):
    return render(request, "restaurants/home.html")

class RestaurantSignupView(View):

    def get(self,*args, **kwargs):
        user_form = SignupForm()
        restaurant_form = RestaurantForm()
      
        return render(self.request, "restaurants/signup.html", {
            'user_form' : user_form,
            'restaurant_form' : restaurant_form
        })
    
    def post(self, *args, **kwargs):
        user_form = SignupForm(self.request.POST or None)
        restaurant_form = RestaurantForm(self.request.POST, self.request.FILES)
   
        if user_form.is_valid() and restaurant_form.is_valid():
            new_user = User.objects.create_user(username=user_form.cleaned_data['username'],
                                                email=user_form.cleaned_data['email'],
                                                password=user_form.cleaned_data['password1'])
           
            new_restaurant_form = Restaurant(
                user = new_user,
                name = restaurant_form.cleaned_data.get('name'),
                phone = restaurant_form.cleaned_data.get('phone'),
                logo = restaurant_form.cleaned_data.get('logo'),
                address = restaurant_form.cleaned_data.get('address')
            )
            new_restaurant_form.save()         
            print(restaurant_form)
            login(self.request,authenticate(
                username = user_form.cleaned_data['username'],
                password = user_form.cleaned_data['password1']
            ))

            return redirect("foodapp:home")
        
        return render(self.request, "restaurants/signup.html", {
            'form' : user_form,
            'restaurant_form' : restaurant_form
        })
