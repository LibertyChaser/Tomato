from django.db import models

# Create your models here.

class Customer(models.Model):
    contact = models.CharField(max_length=64)
    email = models.EmailField()
    name = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    identity = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    discount = models.DecimalField()


class Staff(models.Model):
    Job = (
        ('r', 'receptionist'),
        ('m', 'manager'),
    )
    contact = models.CharField(max_length=64)
    email = models.EmailField()
    name = models.CharField(max_length=64)
    # username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    # identity = models.CharField(max_length=64)
    job = models.CharField(
        max_length=1,
        choices=Job,
        default='m',
    )


class RoomType(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    # mianji
    base_price = models.DecimalField()


class Room(models.Model):
    State = (
        'm', 'maintenance',
        'a', 'available',
        'b', 'booked',
    )
    room_number = models.SmallIntegerField()
    floor = models.SmallIntegerField()
    available = models.CharField(
        max_length=1,
        choices=State,
        default='a',
    )
    room_type = models.ForeignKey(RoomType)
    
    
class Order(models.Model):
    time = models.DateTimeField()
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room_type = models.ForeignKey(RoomType)
    room_number = models.ForeignKey(Room)
    price = models.DecimalField()
    # creator = models.ForeignKey(Customer)
    customer = models.ForeignKey(Customer)


