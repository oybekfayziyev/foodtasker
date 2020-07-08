from django.shortcuts import render, redirect
from django.http import HttpResponse
from allauth.account.views import SignupView
from allauth.account.utils import complete_signup
from allauth.account import app_settings
from .forms import AccountForm, RestaurantForm, UserForm, MealForm
from django.views.generic import View, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Restaurant, Meal, Order, Driver
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Sum, Count, Case, When

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

class AccountView(LoginRequiredMixin,View):    
    
    def get(self, *args, **kwargs):
        profile = User.objects.get(id = self.request.user.id)
        restaurant = Restaurant.objects.get(user=self.request.user)
        context = {
            'form' : profile,
            'restaurant_form' : restaurant
        }

        return render(self.request, 'restaurants/account.html',context)

    def post(self, *args, **kwargs):
        user = User.objects.get(id = self.request.user.id)
        restaurant = Restaurant.objects.get(user=self.request.user)
        username = self.request.POST.get('username')
        first_name = self.request.POST.get('first_name')
        last_name = self.request.POST.get('last_name')
        email = self.request.POST.get('email')
        phone = self.request.POST.get('phone')
        photo = self.request.POST.get('photo')
        address = self.request.POST.get('address')
         
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        restaurant.phone = phone
        restaurant.photo = photo
        restaurant.address = address
        user.save()
        restaurant.save()       

        return redirect("foodapp:restaurant-account")

class OrderView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        form = Order.objects.filter(restaurant = self.request.user.restaurant).order_by('-id')
        return render(self.request, 'restaurants/order.html', {'orders' : form})

    def post(self,*args, **kwargs):
        
        order = Order.objects.get(id = self.request.POST['id'],restaurant = self.request.user.restaurant)
        if order.status == order.COOKING:
            order.status = order.READY
            order.save()

            return redirect('foodapp:restaurant-order')

class MealView(LoginRequiredMixin,View):
    
    def get(self, *args, **kwargs):
        meal = Meal.objects.filter(restaurant = self.request.user.restaurant).order_by('-id')
        return render(self.request, 'restaurants/meal.html', {'meals' : meal})

    
class ReportView(LoginRequiredMixin,View):
    
    def get(self, *args, **kwargs):

        from datetime import timedelta, time
        revenue = []
        orders = []

        today = timezone.now()
        current_weekdays = [today + timedelta(days=i) for i in range(0 - today.weekday(),7-today.weekday())]

        for day in current_weekdays:
            current_orders = Order.objects.filter(
                restaurant = self.request.user.restaurant,
                status = Order.DELIVERED,
                created_at__day = day.day,
                created_at__year = day.year,
                created_at__month = day.month
            )

            revenue.append(sum(order.total for order in current_orders))
            orders.append(current_orders.count())
        

        #  TOP 3 MEALS
        top_meals = Meal.objects.filter(restaurant = self.request.user.restaurant).annotate(total_order=Sum('orderdetail__quantity'))\
                                        .order_by('-total_order')[:3]
        
        meal = {
            "labels" : [meal.name for meal in top_meals],
            "data" : [meal.total_order or 0 for meal in top_meals]
        }

        # TOP 3 DRIVERS

        top_driver = Driver.objects.annotate(
            total_order = Count(
                Case(
                    When(order__restaurant = self.request.user.restaurant,then = 1)
                )
            )
        ).order_by('-total_order')[:3]
        
        driver = {
            'labels' : [driver.user.get_full_name() for driver in top_driver],
            'data' : [driver.total_order for driver in top_driver]
        }

        context = {
            "revenue" : revenue,
            "orders" : orders,
            "meal" : meal,
            'driver' : driver
        }
        return render(self.request,'restaurants/report.html',context)

class AddMealView(LoginRequiredMixin,View):
    
    def get(self, *args, **kwargs):
        form = MealForm()
        context = {
            'form' : form
        }
        return render(self.request, 'restaurants/add_meal.html',context)
    
    def post(self, *args, **kwargs):

        form = MealForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.restaurant = self.request.user.restaurant
            new_form.save()

            return redirect('foodapp:restaurant-meal')
        
        return render(self.request, 'restaurants/add_meal.hmtl')

@login_required(redirect_field_name='/accounts/login/')
def MealEdit(request, meal_id):
    form = MealForm(instance=Meal.objects.get(id=meal_id))
     
    if request.method == "POST":
        form = MealForm(request.POST,request.FILES, instance=Meal.objects.get(id=meal_id))
     
        if form.is_valid():                   
            form.save()
            
            return redirect("foodapp:restaurant-meal")
    
    return render(request, 'restaurants/edit_meal.html', {'meals' : form })


    
   

