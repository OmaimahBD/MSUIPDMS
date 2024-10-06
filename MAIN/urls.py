
from django.urls import path
from . import views 


urlpatterns = [
    path('IPDMS', views.IPDMS, name='IPDMS'),
    path('vison', views.vision, name='vision'),
    path('mission', views.mission, name='mission'),
    path('goals', views.goals, name='goals'),
    path('objectives', views.objectives, name='objectives'),
    path('copyright', views.copyright, name='copyright'),
    path('patent', views.patent, name='patent'),
    path('trademark', views.trademark, name='trademark'),
    path('about', views.about, name='about'),
    path('policy', views.policy, name='policy'),
    path('admincoorpolicy', views.admincoorpolicy, name='admincoorpolicy'),
    path('admincoorabout', views.admincoorabout, name='admincoorabout'),


   path('admincoorroom', views.admincoorroom, name='admincoorroom'),
   path('admincoorroom2', views.admincoorroom2, name='admincoorroom2'),
   path('AdmincoorIntellectualProperty/<str:pk>/', views.admincoorintellectualProperty, name='AdmincoorIntellectualProperty'),
   path('IntellectualPropertyPage/', views.admincoorIntellectualPropertyPage, name='IntellectualPropertyPage'),
 
    
   
] 