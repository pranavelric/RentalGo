"""rentalgo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('<int:product_id>', views.detail, name='detail'),
    path('order/<int:product_id>', views.new_order, name='new_order'),
    path('payment_status/', views.verify_payment, name='status'),
    path('buy_payment_status/', views.buy_payment, name='buy_status'),
    path('buyorder/<int:product_id>', views.buy_order, name='buy_order'),

]
