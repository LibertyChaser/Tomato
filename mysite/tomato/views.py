# from django.core.checks import messages
from django.db.models.query import QuerySet
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import ListView
import datetime
from dateutil.parser import parse
from django.http import JsonResponse

from .models import *

Discount = {
    'g': 1.0,
    'v': 0.9,
}

def get_user_context(request):
    context = dict()

    try:
        loggedin_user_contact = request.session['contact']
        role = request.session['role']
        
        if role == 'staff':
            context['uu'] = get_object_or_404(Staff, contact=loggedin_user_contact)
            context['role'] = 'staff'
            
        elif role == 'customer':
            context['uu'] = get_object_or_404(Customer, contact=loggedin_user_contact)
            context['role'] = 'customer'
            
    except:
        context['uu'] = ''
        context['role'] = ''
        
    return context


def index(request):
    context = get_user_context(request)

    return render(
        request,
        'tomato/index.html',
        context
    )
    
    
def login(request):
    context = get_user_context(request)

    if context['uu'] != '':
        return HttpResponseRedirect('/')
    
    if request.method == 'POST':
        contact = request.POST['contact']
        password = request.POST['password']
        role = ''
        matches = ''
        
        try:
            get_object_or_404(Staff, contact=contact)
            role = 'staff'
            
        except:
            try:
                get_object_or_404(Customer, contact=contact)
                role = 'customer'
                
            except:
                context['uu'] = ''
                context['role'] = ''
                context['message'] = 'Contact doesn\'t exist!'

        if role == 'customer':
            matches = Customer.objects.filter(contact=contact)

        elif role == 'staff':
            matches = Staff.objects.filter(contact=contact)

        if len(matches) != 0 :
            if password == matches[0].password:
                request.session['role'] = role
                request.session['contact'] = matches[0].contact
                return HttpResponseRedirect('/')
            
            else:
                context['message'] = 'Password wrong.'
    
    return render(
        request,
        'tomato/login.html',
        context,
    )
    
    
def logout(request):
    try:
        del request.session['contact']
        del request.session['role']
    except KeyError:
        return HttpResponseRedirect('/')
    
    return HttpResponseRedirect('/')


def register(request):
    context = get_user_context(request)
    
    if context['uu'] != '':
        return HttpResponseRedirect('/')
    
    context['draft'] = {}
    context['message'] = []
    
    if request.method == 'POST':
        context['draft']['name'] = request.POST['name']
        context['draft']['contact'] = request.POST['contact']

        context['draft']['password1'] = request.POST['password1']
        context['draft']['password2'] = request.POST['password2']
        
        if len(context['draft']['name']) > 64or len(context['draft']['name']) == 0:
            if len(context['draft']['name']) > 64:
                context['message'].append('Name is too long!')
            else:
                context['message'].append('Name can\'t be empty!')

        if len(context['draft']['contact']) > 64 or len(context['draft']['contact']) == 0:
            if len(context['draft']['contact']) > 64:
                context['message'].append('Contact is too long!')
            else:
                context['message'].append('Contact can\'t be empty!')
        
        matches_customer = Customer.objects.filter(contact=context['draft']['contact'])
        matches_staff = Staff.objects.filter(contact=context['draft']['contact'])
        
        if len(matches_customer) != 0 or len(matches_staff) != 0:
            context['message'].append('Contact already exist!')
            
        if context['draft']['password1'] != context['draft']['password2'] or \
                len(context['draft']['password1']) > 64 or \
                len(context['draft']['password1']) == 0:
            context['message'].append('Password Error!')
        
        if len(context['message']) == 0:
            context['order'] = Customer()
            context['order'].name = context['draft']['name']
            context['order'].contact = context['draft']['contact']
            context['order'].password = context['draft']['password1']
            context['order'].save()

            context['draft'] = {}
            context['message'].append('Register Successfully!')
            
    return render(
        request,
        'tomato/register.html',
        context,
    )


def dashboard(request):
    context = get_user_context(request)
    
    if context['uu'] == '':
        return HttpResponseRedirect('/')
    
    return render(
        request,
        'tomato/dashboard.html',
        context,
    )
    
    
def edit_profile(request):
    context = get_user_context(request)
    
    if context['uu'] == '':
        return HttpResponseRedirect('/')
    
    if request.method == 'POST':
        post_contact = request.POST['contact']
        post_email = request.POST['email']
        post_name = request.POST['name']
        post_username = request.POST['username']
        post_password1 = request.POST['password1']
        post_password2 = request.POST['password2']
        post_identity = request.POST['identity']
        post_bank_card = request.POST['bank_card']
        post_description = request.POST['description']
        context['message'] = []
        
        if len(post_contact) > 64 or len(post_contact) == 0:
            if len(post_contact) > 64:
                context['message'].append('Contact is too long!')
            else:
                context['message'].append('Contact can\'t be empty!')
                
        if len(post_name) > 64 or len(post_name) == 0:
            if len(post_name) > 64:
                context['message'].append('Name is too long!')
            else:
                context['message'].append('Name can\'t be empty')

        if len(context['message']) == 0:
            matches_customer = Customer.objects.filter(contact=post_contact)
            matches_staff = Staff.objects.filter(contact=post_contact)

            if (len(matches_customer) != 0 or len(matches_staff) != 0) and context['uu'].contact != post_contact:
                context['message'].append('Contact already exist.')

            if len(context['message']) == 0:
                if post_password1 == post_password2 and 0 < len(post_password1) <= 64:
                    context['uu'].contact = post_contact
                    context['uu'].email = post_email
                    context['uu'].name = post_name
                    context['uu'].username = post_username
                    context['uu'].password = post_password1
                    context['uu'].identity = post_identity
                    context['uu'].bank_card = post_bank_card
                    context['uu'].description = post_description
                    context['uu'].save()
                    request.session['contact'] = post_contact
                    context['message'].append('Infomation updated!')

                else:
                    if len(post_password1) == 0:
                        context['message'].append('Password can\'t be empty!')
                    elif len(post_password1) > 64:
                        context['message'].append('Password is too long!')
                    else:
                        context['message'].append('Passwords don\'t match!')
    
    return render(
        request,
        'tomato/edit_profile.html',
        context,
    )


def room_types(request):
    context = get_user_context(request)
    
    context['room_types'] = RoomType.objects.all()
    
    if context['role'] == 'customer':
        Level = (
            ('g', 'general_user'),
            ('v', 'vip_ueser'),
        )
        level = context['uu'].level
        for item in context['room_types']:
            item.price *= (item.base_price * Discount[level])
    
    return render(
        request,
        'tomato/room_types.html',
        context,
    )
    
    
def room_type_edit(request, room_type_id):
    context = get_user_context(request)
    
    if context['role'] != 'staff':
        return HttpResponseRedirect('/')
    
    context['room_type'] = get_object_or_404(RoomType, pk=room_type_id)
    
    return render(
        request,
        'tomato/room_type_edit.html',
        context,
    )
  
    
def room_type_detail(request, room_type_id):
    context = get_user_context(request)
    
    if context['role'] != 'staff':
        return HttpResponseRedirect('/')
    
    context['room_type'] = get_object_or_404(RoomType, pk=room_type_id)
    
    return render(
        request,
        'tomato/room_type_detail.html',
        context,
    )
    
    
def room_type_order(request, room_type_id):
    context = get_user_context(request)
    
    if context['role'] != 'customer':
        return HttpResponseRedirect('/')
    
    context['room_type'] = get_object_or_404(RoomType, pk=room_type_id)
    
    level = context['uu'].level
    context['room_type'].price *= (context['room_type'].base_price * Discount[level])
    
    if context['role'] != 'customer':
        return HttpResponseRedirect('/')
    
    context['draft'] = {}
    context['message'] = []
    
    if request.method == 'POST':
        context['draft']['check_in_date'] = request.POST['check_in_date']
        context['draft']['check_out_date'] = request.POST['check_out_date']
        
        if context['draft']['check_in_date'] < datetime.date.today().strftime('%Y-%m-%d'):
            context['message'].append('Check in time can\'t before todaty!')
            
        if context['draft']['check_in_date'] >= context['draft']['check_out_date']:
            context['message'].append('Check in time can\'t before check out time!')
        
        
        check_in_day = parse(context['draft']['check_in_date'])
        check_out_day = parse(context['draft']['check_out_date'])
        diff = check_out_day - check_in_day
        
        context['order'] = Order()
        context['order'].price = context['room_type'].price * diff.days
        context['order'].bank_card = request.POST['bank_card']
        
        if (check_in_day - datetime.datetime.today()).days > 30:
            context['order'].price *= 0.75
            context['order'].state = 'r'
            bankcard = get_object_or_404(BankCard, card_id=context['order'].bank_card)
            if bankcard.balance >= context['order'].price:
                bankcard.balance -= context['order'].price
                bankcard.save()
            else:
                context['message'].append('Balance Not Enough!')
            
        if len(context['message']) == 0:
            context['order'].time = datetime.datetime.now()
            context['order'].check_in_date = context['draft']['check_in_date']
            context['order'].check_out_date = context['draft']['check_out_date']
            context['order'].room_type = context['room_type']
            context['order'].room_number = get_object_or_404(Room, pk=13)
            
            context['order'].customer = context['uu']
            context['order'].save()
            context['message'].append('Order Successfully!')
            
    return render(
        request,
        'tomato/room_type_order.html',
        context,
    )
    
    
def rooms(request):
    context = get_user_context(request)
    
    if context['role'] != 'staff':
        return HttpResponseRedirect('/')
    
    context['room_types'] = RoomType.objects.all()

    return render(
        request,
        'tomato/rooms.html',
        context,
    )
    
    
def my_orders(request):
    context = get_user_context(request)
    
    if context['role'] != 'customer':
        return HttpResponseRedirect('/')
    
    context['all_orders'] = Order.objects.filter(customer_id=context['uu'].id)
    context['room_types'] = RoomType.objects.all()
    
    return render(
        request,
        'tomato/my_orders.html',
        context,
    )
    

def order_cancel(request, order_id):
    context = get_user_context(request)
    
    context['order'] = get_object_or_404(Order, pk=order_id)

    if context['role'] == '' or context['order'].state == 'f' or context['order'].state == 'c':
        return HttpResponseRedirect('/')
    
    if context['role'] == 'customer' and context['uu'].id != context['order'].customer.id:
        return HttpResponseRedirect('/')
    
    context['message'] = []
    
    check_in_day = context['order'].check_in_date
    
    if context['order'].state != 'r' and (check_in_day - datetime.date.today()).days >= 3:
    
        check_out_day = context['order'].check_out_date
        diff = check_out_day - check_in_day
        context['order'].price /= diff.days
        
        bankcard = get_object_or_404(BankCard, card_id=context['order'].bank_card)
        if bankcard.balance >= context['order'].price:
            bankcard.balance -= context['order'].price
            bankcard.save()
        else:
            context['message'].append('Balance Not Enough!')

    
    context['order'].state = 'c'
    context['order'].save()
            
    return render(
        request,
        'tomato/order_change.html',
        context,
    )


def order_detail(request, order_id):
    context = get_user_context(request)
    
    if context['role'] == '':
        return HttpResponseRedirect('/')
    
    context['order'] = get_object_or_404(Order, pk=order_id)
    
    if context['role'] == 'customer' and context['uu'].id != context['order'].customer.id:
        return HttpResponseRedirect('/')
    
    if context['order'].check_in_date == datetime.date.today() and context['order'].state != 'i':
        context['flag'] = 'check_in'
    
    elif context['order'].check_out_date == datetime.date.today() and context['order'].state == 'i':
        context['flag'] = 'check_out'
    
    return render(
        request,
        'tomato/order_detail.html',
        context,
    )
    

def order_change(request, order_id):
    context = get_user_context(request)
    
    context['order'] = get_object_or_404(Order, pk=order_id)

    if context['role'] == '' or context['order'].state == 'f' or context['order'].state == 'c':
        return HttpResponseRedirect('/')
    
    if context['role'] == 'customer' and context['uu'].id != context['order'].customer.id:
        return HttpResponseRedirect('/')
    
    level = context['uu'].level
    context['order'].room_type.price *= (context['order'].room_type.base_price * Discount[level])
    
    context['message'] = []
    
    if request.method == 'POST':
        post_check_in_date = request.POST['check_in_date']
        post_check_out_date = request.POST['check_out_date']
        
        if post_check_in_date < datetime.date.today().strftime('%Y-%m-%d'):
            context['message'].append('Check in time can\'t before todaty!')
            
        if post_check_in_date >= post_check_out_date:
            context['message'].append('Check in time can\'t before check out time!')
        
        if len(context['message']) == 0:
            
            context['order'].check_in_date = post_check_in_date
            context['order'].check_out_date = post_check_out_date
            
            check_in_day = parse(post_check_in_date)
            check_out_day = parse(post_check_out_date)
            diff = check_out_day - check_in_day
            
            context['order'].price = context['order'].room_type.price * diff.days
            context['order'].bank_card = request.POST['bank_card']
            
            if (check_in_day - datetime.datetime.today()).days > 30:
                context['order'].price *= 0.75
                context['order'].state = 'r'
            
            context['order'].save()
            
            context['message'].append('Order Successfully!')
            
    return render(
        request,
        'tomato/order_change.html',
        context,
    )


def order_check_in(request, order_id):
    context = get_user_context(request)
    
    context['order'] = get_object_or_404(Order, pk=order_id)

    if context['role'] == '' or context['order'].state == 'f' or context['order'].state == 'c':
        return HttpResponseRedirect('/')
    
    if context['role'] != 'staff':
        return HttpResponseRedirect('/')
    
    context['room_choices'] = Room.objects.filter(available='a', room_type=context['order'].room_type)
    
    if request.method == 'POST':
        room_choice = request.POST['check_in_room']
        room = get_object_or_404(Room, pk=room_choice)
        room.available = 'b'
        room.save()
        
        context['order'].state = 'i'
        context['order'].room_number = room
        context['order'].save()
        
        context['message'] = []
        context['message'].append('Check In Successfully!')
            
    return render(
        request,
        'tomato/order_check_in.html',
        context,
    )
    
    
def order_check_out(request, order_id):
    context = get_user_context(request)
    
    context['order'] = get_object_or_404(Order, pk=order_id)

    if context['role'] == '' or context['order'].state == 'f' or context['order'].state == 'c':
        return HttpResponseRedirect('/')
    
    if context['role'] != 'staff':
        return HttpResponseRedirect('/')
    
    context['flag'] = 'check_out'
    
    context['message'] = []
        
    bankcard = get_object_or_404(BankCard, card_id=context['order'].bank_card)
    if bankcard.balance >= context['order'].price:
        bankcard.balance -= context['order'].price
        bankcard.save()
    else:
        context['message'].append('Balance Not Enough!')
    
    if len(context['message']) == 0:
        room = get_object_or_404(Room, pk=context['order'].room_number.id)
        room.available = 'a'
        room.save()
    
        context['order'].state = 'f'
        context['order'].save()
        
        context['message'] = []
        context['message'].append('Check Out Successfully!')
            
    return HttpResponseRedirect('/today/check/')
    
    
def today_check(request):
    context = get_user_context(request)

    if context['role'] == '':
        return HttpResponseRedirect('/')
    
    if context['role'] != 'staff':
        return HttpResponseRedirect('/')
    
    context['all_check_in'] = Order.objects.filter(check_in_date=datetime.date.today().strftime('%Y-%m-%d'))
    context['all_check_out'] = Order.objects.filter(check_out_date=datetime.date.today().strftime('%Y-%m-%d'))
    
    return render(
        request,
        'tomato/today_check.html',
        context,
    )
        
        
def orders(request):
    context = get_user_context(request)
    
    if context['uu'].job != 'm':
        return HttpResponseRedirect('/')
    
    context['orders'] = Order.objects.all()
    
    return render(
        request,
        'tomato/orders.html',
        context,
    )
    
def dd():
    today = datetime.date.today()
    final = today + datetime.timedelta(hours=30*24) # 第 31 天
    orders = Order.objects.exclude(state='c').filter(check_out_date__gt=today, check_in_date__lte=final)
    
    cnt = [0] * (30 + 1)
    revenue = [0] * (30 + 1)
    
    for order in orders:
        a = (order.check_in_date - today).days
        if a < 0:
            a = 0
        b = (order.check_out_date - today).days
        if b > 30:
            b = 30
        cnt[a] += 1  # 前缀和
        cnt[b] -= 1  # 前缀和
        avg_price = order.price / order.days()
        revenue[a] += avg_price
        revenue[b] -= avg_price
    
    for i in range(1, len(cnt)):
        cnt[i] += cnt[i - 1]
        revenue[i] += revenue[i - 1]
    
    return cnt, revenue

def overview(request):
    context = get_user_context(request)

    if context['role'] == '':
        return HttpResponseRedirect('/')
    
    if context['role'] != 'staff':
        return HttpResponseRedirect('/')
    
    cnt, revenue = dd()
    
    context['data'] = []
    
    today = datetime.date.today()
    for val1, val2 in zip(cnt, revenue):
        context['data'].append({'date': today, 'rooms': val1, 'sum': val2})
        today + datetime.timedelta(hours=24) # 第 31 天
    
    return render(
        request, 
        'tomato/overview.html',
        context,
    )


# map to '/ordered_rooms_stat/' with name 'ordered_rooms_stat'
def ordered_rooms_stat(request):
    # 查询未来 30 天内会入住或者正在入住的订单
    context = get_user_context(request)

    if context['role'] == '':
        return HttpResponseRedirect('/')
    
    if context['uu'].job != 'm':
        return HttpResponseRedirect('/')
    
    cnt, revenue = dd()
    
    return JsonResponse(data={
        'labels': [i for i in range(30)],
        'cnt': cnt[0:-1],
        'revenue': revenue[0:-1],
    })
