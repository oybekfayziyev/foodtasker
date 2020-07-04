from django.shortcuts import render, redirect
from django.http import HttpResponse
from allauth.account.views import SignupView
from allauth.account.utils import complete_signup
from allauth.account import app_settings
from .forms import AccountForm, RestaurantForm,UserForm
from django.views.generic import View, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Restaurant
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def HomeView(request):
    return render(request, "restaurants/home.html")

class MySignupView(SignupView):
    

    def get_context_data(self, **kwargs):           
        context = super(MySignupView, self).get_context_data(**kwargs)
        context['restaurant_form'] = RestaurantForm() # add form to context
        print(context)
        return context
    
    def form_valid(self, form):
        # By assigning the User to a property on the view, we allow subclasses
        # of SignupView to access the newly created User instance
        print('retaurant',self.restaurant_form)   
        print('retaurant',form)   
        self.restaurant_form = form.save(self.request)   
        print('retaurant',self.restaurant_form)      
        return complete_signup(
            self.request, self.user,
            app_settings.EMAIL_VERIFICATION,
            self.get_success_url())
        
        

class RestaurantSignupView(View):

    def get(self,*args, **kwargs):
        user_form = User()
        restaurant_form = RestaurantForm()
        users = User.objects.all()
        for user in users:
            print(user.id)
       
        return render(self.request, "restaurants/signup.html", {
            'user_form' : user_form,
            'restaurant_form' : restaurant_form
        })
      
    def post(self, *args, **kwargs):
        user_form = User()
        username = self.request.POST.get('username')
        first_name = self.request.POST.get('firstname')
        last_name = self.request.POST.get('lastname')
        email = self.request.POST.get('email')
        password1 = self.request.POST.get('password1')
        password2 = self.request.POST.get('password2')
        restaurant_form = RestaurantForm(self.request.POST, self.request.FILES)
        print(restaurant_form)
        if restaurant_form.is_valid():          
            new_user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password1,
                                                first_name = first_name,
                                                last_name = last_name)           
            new_restaurant_form = Restaurant(
                user = new_user,              
                name = restaurant_form.cleaned_data.get('name'),
                phone = restaurant_form.cleaned_data.get('phone'),
                logo = restaurant_form.cleaned_data.get('logo'),
                address = restaurant_form.cleaned_data.get('address')
            )
            new_restaurant_form.save()         
            print('restaurant',restaurant_form)
            login(self.request,authenticate(
                username = username,
                password = password1
            ))

            return redirect("foodapp:home")
        
        return render(self.request, "restaurants/signup.html", {
            'form' : user_form,
            'restaurant_form' : restaurant_form
        })

class AccountView(LoginRequiredMixin,TemplateView):    
    template_name = 'restaurants/account.html'

class OrderView(LoginRequiredMixin,TemplateView):
    template_name = 'restaurants/order.html'

class MealView(LoginRequiredMixin,TemplateView):
    template_name = 'restaurants/meal.html'

class ReportView(LoginRequiredMixin,TemplateView):
    template_name = 'restaurants/report.html'