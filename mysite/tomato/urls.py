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
    path('room_type/<int:room_type_id>/edit/', views.room_type_edit, name='room_type_edit'),
    path('room_type/<int:room_type_id>/detail/', views.room_type_detail, name='room_type_detail'),
    path('room_type/<int:room_type_id>/order/', views.room_type_order, name='room_type_order'),
    path('rooms/', views.rooms, name='rooms'),
    
    path('my_orders/', views.my_orders, name='my_orders'),
    path('orders/', views.orders, name='orders'),
    path('order/<int:order_id>/detail/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/change/', views.order_change, name='order_change'),
    path('order/<int:order_id>/cancel/', views.order_cancel, name='order_cancel'),
    path('order/<int:order_id>/check_in/', views.order_check_in, name='order_check_in'),
    path('order/<int:order_id>/check_out/', views.order_check_out, name='order_check_out'),
    
    path('today/check/', views.today_check, name='today_check'),
    
    path('overview/', views.overview, name='overview'),
    path('ordered_rooms_stat/', views.ordered_rooms_stat, name='ordered_rooms_stat'),
    
]