from django.urls import path

from . import views

app_name = 'tomato'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    path('rooms/', views.rooms, name='rooms'),
]