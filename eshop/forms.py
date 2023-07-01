from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    #
    class Meta:
        model = Product
        exclude = ["user"]


class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    #
    class Meta:
        model = Customer
        exclude = ["user"]


class OrderForm(forms.ModelForm):
    fname = forms.CharField(max_length=255)
    lname = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=255)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=255)
    state = forms.CharField(max_length=255)
    country = forms.CharField(max_length=255)
    pincode = forms.CharField(max_length=255)

    #
    class Meta:
        model = Order
        exclude = ['user', 'status', 'total_price', 'tracking_no', 'created_at']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
