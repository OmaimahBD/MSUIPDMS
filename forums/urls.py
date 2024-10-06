from django.urls import path
from . import views 



urlpatterns = [
       path('forums/', views.forums, name='forums'),
        
   
]