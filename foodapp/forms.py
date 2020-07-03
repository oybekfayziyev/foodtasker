from django import forms
from .models import Restaurant
from allauth.account.forms import LoginForm, SignupForm

class UserForm(SignupForm):
    first_name = forms.CharField(max_length=30, widget = forms.TextInput(attrs = {
        'placeholder' : 'Enter your name'
    }))
    last_name = forms.CharField(max_length=30, widget = forms.TextInput(attrs={
        'placeholder' : 'Enter your surname'
    }))

    def save(self,request):
        user = super(UserForm,self).save(request)     
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        
        return user

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'phone','address','logo']