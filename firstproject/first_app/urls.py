from django.urls import path
from first_app import views

app_name = 'first_app'
urlpatterns = [
    path('signup/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
]
