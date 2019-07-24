from django import forms
from django.contrib.auth.models import User
from .models import Product, Order, BuyOrder

class ProdForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('prod_name','description','img1','img2','quantity','dprice','wprice','mprice','available_for_selling','sprice','city_choice')
        labels = {
                    'prod_name': 'Product Name',
                    'description': 'Description',
                    'quantity': 'Quantity',
                    'img1': 'Image 1',
                    'img2': 'Image 2',
                    'dprice': 'Rent per Day',
                    'wprice': 'Rent per Week',
                    'mprice': 'Rent per Month',
                    'sprice': 'Selling Price(Fill if available for sale)',
                    'city_choice': 'This Product is available in',
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('address','zip_code','contact','date_range',)
        labels = {
                    'date_range': 'Date Range',
                    'address': 'Address',
                    # 'city': 'City',
                    'zip_code': 'Zip Code',
                    'contact': 'Mobile Number',
        }

class BuyForm(forms.ModelForm):
    class Meta:
        model = BuyOrder
        fields = ('address','zip_code','contact',)
        labels = {
                    'address': 'Address',
                    # 'city': 'City',
                    'zip_code': 'Zip Code',
                    'contact': 'Mobile Number',
        }
