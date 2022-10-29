from itertools import product
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all().order_by('brand')


    context = {'products': products , 'cartItems':cartItems  }
    return render(request, 'store/store.html', context)

def deals(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'cartItems':cartItems  }
    return render(request, 'store/deals.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order , 'cartItems':cartItems }
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    isMulti =  data['isMulti']
    productId = data['productId']
    action = data['action']

    print('action :>>',  action)
    if isMulti:

        print('Logged in User update item view is Multi >>>', isMulti)
        price = data['price']
        quantity = data['quantity']
        print('myquantity in views:  >>', quantity , 'price : £', price , action)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem,created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'delete':
        orderItem.quantity = 0

    if action =='add':
        if isMulti:
            print("actual price", price)
            orderItem.product.price = price
            orderItem.quantity = int(quantity) + int(orderItem.quantity)
        else:
            orderItem.quantity = (orderItem.quantity + 1 )

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1 )

    orderItem.save()

    if int(orderItem.quantity)  <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added--I reside in view', safe=False)


def processOrder(request):

    order.shipping==True
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    else:
        customer, order = guestOrder(request , data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
        order.save()

    if order.shipping==True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )

        #send confirmation email to user & admin to process order

    return JsonResponse('Payment Complete !', safe=False)








    