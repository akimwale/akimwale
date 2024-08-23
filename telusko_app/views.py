from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
# from .filter import OrderFilter
from django.contrib.auth.decorators import login_required

from .decorators import allowed_users
import logging
from accounts.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

# logger = logging.getLogger(__name__)
def index(request):
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            return render(request, 'index.html', {'customer': customer})
        else:
            return render(request, 'index.html', {'error': 'No customer profile found.'})
    return render(request, 'index.html')



def about(request):
   if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            return render(request, 'about.html', {'customer': customer})
        else:
            return render(request, 'about.html', {'error': 'No customer profile found.'})
   return render(request, 'about.html')

def blog(request):
   if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            return render(request, 'blog.html', {'customer': customer})
        else:
            return render(request, 'blog.html', {'error': 'No customer profile found.'})
   return render(request, 'blog.html')

def commune(request):
   if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            return render(request, 'contact.html', {'customer': customer})
        else:
            return render(request, 'contact.html', {'error': 'No customer profile found.'})
   return render(request, 'contact.html')



def service(request):
   if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            return render(request, 'service.html', {'customer': customer})
        else:
            return render(request, 'service.html', {'error': 'No customer profile found.'})
   return render(request, 'service.html')

def team(request):
   if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            return render(request, 'team.html', {'customer': customer})
        else:
            return render(request, 'team.html', {'error': 'No customer profile found.'})
   return render(request, 'team.html')

def testimonies(request):
   if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            return render(request, 'testimonial.html', {'customer': customer})
        else:
            return render(request, 'testimonial.html', {'error': 'No customer profile found.'})
   return render(request, 'testimonial.html')








# def add(request):
#     val1 = int(request.POST['num1'])
#     val2 = int(request.POST['num2'])
#     sum = val1 + val2
#     return render(request, 'result.html', {'result': sum})