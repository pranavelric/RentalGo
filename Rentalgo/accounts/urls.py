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
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup.as_view(), name='signup'),
    path('login/', views.user_login ,name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/',views.user_profile, name='profile'),
    path('getKyc/',views.getKyc, name='getKyc'),
    path('delete/<int:product_id>/', views.delete_product, name='delete'),
    path('orders/',views.orders, name='orders'),
]
