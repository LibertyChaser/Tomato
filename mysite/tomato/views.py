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
import re

from .models import *

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
            new = Customer()
            new.name = context['draft']['name']
            new.contact = context['draft']['contact']
            new.password = context['draft']['password1']
            new.save()

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
        Discount = {
            'g': 1.0,
            'v': 0.8,
        }
        level = context['uu'].level
        for item in context['room_types']:
            item.price *= (item.base_price * Discount[level])
    
    return render(
        request,
        'tomato/room_types.html',
        context,
    )
    
    
def room_type_order(request, room_type_id):
    context = get_user_context(request)
    
    if context['role'] != 'customer':
        return HttpResponseRedirect('/')
    
    context['room_type'] = get_object_or_404(RoomType, pk=room_type_id)
    Discount = {
        'g': 1.0,
        'v': 0.8,
    }
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
        
        if len(context['message']) == 0:
            new = Order()
            new.time = datetime.datetime.now()
            new.check_in_date = context['draft']['check_in_date']
            new.check_out_date = context['draft']['check_out_date']
            new.room_type = context['room_type']
            new.room_number = get_object_or_404(Room, pk=13)
            
            check_in_day = parse(context['draft']['check_in_date'])
            check_out_day = parse(context['draft']['check_out_date'])
            diff = check_out_day - check_in_day
            
            new.price = context['room_type'].price * diff.days
            
            if (check_in_day - datetime.datetime.today()).days > 30:
                new.price *= 0.7
            
            new.customer = context['uu']
            new.save()
            context['message'].append('Order Successfully!')
            
    return render(
        request,
        'tomato/room_type_order.html',
        context,
    )
    
    
def rooms(request):
    context = get_user_context(request)
    
    if context['role'] != 'Staff':
        return HttpResponseRedirect('/')
    
    return render(
        request,
        'tomato/rooms.html',
        context,
    )