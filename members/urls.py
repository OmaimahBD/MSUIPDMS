from django.urls import path
from .views import _login, _register
from . import views 



urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views._login, name='login'),
    path('register/', views._register, name='register'),

    path('members/', views.members,name='members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),
        
   
]