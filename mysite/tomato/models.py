from django.db import models


class Customer(models.Model):
    # Discount = {
    #     'g': 1.0,
    #     'v': 0.8,
    # }
    contact = models.CharField(max_length=64)
    email = models.EmailField()
    name = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    identity = models.CharField(max_length=64)
    bank_card = models.IntegerField(default=0)
    description = models.CharField(max_length=128)
    level = models.CharField(
        max_length=1,
        default='g',
    )
    # discount = Discount[str(level)]
    def __str__(self):
        Level = {
            'g': 'general_user',
            'v': 'vip_ueser',
        }
        return "{} {}".format(self.name, Level[self.level])


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
    description = models.CharField(
        max_length=128, 
        default='',
    )
    
    def __str__(self):
        Job = {
            'r': 'receptionist',
            'm': 'manager',
        }
        return "{} {}".format(self.name, Job[self.job])


class RoomType(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    # area = models.DecimalField()
    base_price = models.IntegerField()
    price = models.IntegerField(default=1)
    
    def __str__(self):
        return "{} {} {}".format(self.name, self.base_price, self.description)


class Room(models.Model):
    State = (
        ('m', 'maintenance'),
        ('a', 'available'),
        ('b', 'booked'),
    )
    room_number = models.SmallIntegerField()
    floor = models.SmallIntegerField()
    available = models.CharField(
        max_length=1,
        choices=State,
        default='a',
    )
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    max_guest_num = models.SmallIntegerField(default=1)
    
    def __str__(self):
        return "{} {} {} {}".format(
            self.room_number, 
            self.room_type.name, 
            self.max_guest_num,
            self.available
        )
    
    
class Order(models.Model):
    State = (
        ('p', 'in_progress'),  # yellow
        ('c', 'canceled'),  # red
        ('f', 'finished'),  # gray
        ('r', 'under_reservation'),  # green
    )
    time = models.DateTimeField()
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.IntegerField()
    bank_card = models.IntegerField(default=0)
    # creator = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=1,
        choices=State,
        default='p',
    )
    
    def __str__(self):
        return "{} {} - {} price:{}".format(
            self.customer,
            self.check_in_date, 
            self.check_out_date, 
            self.price,
        )

