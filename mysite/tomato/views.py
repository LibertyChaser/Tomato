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


def rooms(request):
    context = get_user_context(request)
    
    context['room_type'] = RoomType.objects.all()
    
    return render(
        request,
        'tomato/rooms.html',
        context,
    )
    
    