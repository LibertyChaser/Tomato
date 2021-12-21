from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(Order)
admin.site.register(Room)
admin.site.register(RoomType)
