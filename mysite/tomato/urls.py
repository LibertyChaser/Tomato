from django.urls import path

from . import views

app_name = 'tomato'

urlpatterns = [
    path('', views.index, name='index'),
    
    
]