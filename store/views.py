import datetime
import json

import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .utils.jwt_utilts import create_jwt_token, verify_jwt_token

from .models import *

# Create your views here.

def get_login_view(request):
    context = {}
    return render(request, 'auth/login.html', context)

def get_signup_view(request):
    context = {}
    return render(request, 'auth/signup.html', context)

def validate_user(username, email, password, password_confirm):
    if password != password_confirm: 
        return False
    if User.objects.filter(email=email):
        return False
    return True

@csrf_protect
def create_user(request):

    data = json.loads(request.body)
    username = data['userData']['username']
    email = data['userData']['email']
    password = data['userData']['password']
    password_confirm = data['userData']['password_confirm']

    if validate_user(username, email, password, password_confirm):
        user = User.objects.create_user(username, email, password)
        Customer.objects.create(user=user, name=username, email=email)
        return HttpResponse(201)
    else:
        return HttpResponse(400)
    
@csrf_protect
def login(request):
    
    data = json.loads(request.body)
    username = data['userData']['username']
    password = data['userData']['password']

    user = authenticate(username=username, password=password)
    if user:
        auth_login(request, user)
        token = create_jwt_token(user.id)
        return JsonResponse({'Access Token': token}, status=200)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

@csrf_protect   
def logout(request):

    user = request.user
    if user:
        auth_logout(request)
        return HttpResponse(200)
    else:
        return HttpResponse(400)

def store(request):    
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else: 
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0
        }
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/store.html', context)

def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print('Cart:', cart) 
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0
        }
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/cart.html', context)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else: 
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0
        }
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

@csrf_exempt
def updateItem(request):
    if not request.user.is_authenticated:
        return JsonResponse('User is not authenticated')

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove': 
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:   
        print('User is not logged in...')

    return JsonResponse('Payment submitted...', safe=False)

def viewItem(request, product_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else: 
        items = []
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0
        }
        cartItems = order['get_cart_items']

    product = Product.objects.get(id=product_id)
    context = {'product': product, 'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/view.html', context)