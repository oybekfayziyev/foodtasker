from django import forms
from .models import Restaurant, Meal, Order
from allauth.account.forms import LoginForm, SignupForm,ResetPasswordForm
from django.contrib.auth.models import User

class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        
        ## here i add the new fields that i need
        # self.fields["new-field"] = forms.CharField(label='Some label', max_length=100)
        self.fields['email'] = forms.EmailField(widget = forms.EmailInput(attrs={
            'class' : 'input100'
        }))
        

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        print('username ',self.fields)
        ## here i add the new fields that i need
        # self.fields["new-field"] = forms.CharField(label='Some label', max_length=100)
        self.fields['login'] = forms.CharField(widget = forms.TextInput(attrs={
            'class' : 'input100'
        }))
        

class UserForm(SignupForm):    
    
    first_name = forms.CharField(max_length=30, widget = forms.TextInput(attrs = {
        'placeholder' : 'Enter your name'
    }))
    last_name = forms.CharField(max_length=30, widget = forms.TextInput(attrs={
        'placeholder' : 'Enter your surname'
    }))
    
    def save(self,request):
        user = super(UserForm,self).save(request)    
        user.username = self.cleaned_data['username'] 
   
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        
        return user

class AccountForm(forms.ModelForm):    

    phone = forms.CharField(max_length=20)
    photo = forms.ImageField()
    
    class Meta:
        model = User
        fields = ['first_name','last_name','email','phone','photo']

class RestaurantForm(forms.Form):

    name = forms.CharField(max_length=30, widget = forms.TextInput(attrs = {
        'placeholder' : 'Enter your name',
        'class' : 'input100'
    }))
    phone = forms.CharField(max_length=30, widget = forms.TextInput(attrs={
        'placeholder' : 'Enter phone number',
        'class' : 'input100'
    }))
    address = forms.CharField(max_length=30, widget = forms.TextInput(attrs = {
        'placeholder' : 'Enter address',
        'class' : 'input100'
    }))
    logo = forms.ImageField()

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name','description','image','price']




    
    

