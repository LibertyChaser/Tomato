from django.db import models


class Customer(models.Model):
    # Discount = {
    #     'g': 1.0,
    #     'v': 0.9,
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


class Resident(models.Model):
    resident_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return "{} {}".format(
            self.resident_id,
            self.name,
        )
        
    
class Order(models.Model):
    State = (
        ('p', 'in_progress'),  # yellow
        ('c', 'canceled'),  # red
        ('f', 'finished'),  # gray
        ('r', 'under_reservation'),  # green
        ('i', 'checked_in'), # info
    )
    time = models.DateTimeField()
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE)
    price = models.IntegerField()
    bank_card = models.IntegerField(default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=1,
        choices=State,
        default='p',
    )
    
    def days(self):
        return (self.check_out_date - self.check_in_date).days
    
    def __str__(self):
        return "{} {} - {} price:{}".format(
            self.customer,
            self.check_in_date, 
            self.check_out_date, 
            self.price,
        )


class BankCard(models.Model):
    card_id = models.IntegerField(default=0)
    balance = models.IntegerField(default=2000)

    def __str__(self):
        return "Card ID: {} Balance: {}".format(
            self.card_id,
            self.balance, 
        )
        
        
class BasePriceManege(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    ratio = models.DecimalField(decimal_places=4, max_digits=5)
    
    def __str__(self):
        return "Ratio: {}, RoomType: {}, From {} to {} ".format(
            self.ratio,
            self.room_type.name,
            self.start_date,
            self.end_date,
        )
