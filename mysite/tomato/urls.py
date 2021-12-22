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
    
    path('room_types/', views.room_types, name='room_types'),
    path('room_type/<int:room_type_id>/order/', views.room_type_order, name='room_type_order'),
    path('rooms/', views.rooms, name='rooms'),
    
]