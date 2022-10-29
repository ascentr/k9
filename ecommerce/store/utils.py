import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart ={}
        
    # print('Cart:', cart)
    items=[]
    order = { 'get_cart_total':0 , 'get_cart_items':0, 'shipping':True}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)

            if cart[i]['quantity'] >= 20:
                myprice = product.multibuy_price2
            elif cart[i]['quantity'] >= 10:
                myprice = product.multibuy_price
            else:
                myprice = product.price
            

            print('the price comming from cookieCart : <><>' , myprice)

            total =  (myprice * cart[i]['quantity'] )

            # total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total                            
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':myprice,
                    'imageURL':product.imageURL,
                    },
                'quantity':cart[i]['quantity'],
                'get_total':total
                }
            items.append(item)


            order['shipping'] = True
        except:
            pass

    return {'cartItems':cartItems, 'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated & hasattr(request.user, 'customer'):
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems':cartItems, 'order':order, 'items':items}

def guestOrder(request , data):
    print('User is not Authenticated', data)

    # print('COOKIES:', request.COOKIES)
    name= data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    
    customer, created = Customer.objects.get_or_create(
        email=email,
        )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete = False,
        )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        
        orderItem = OrderItem.objects.create(
            product = product,
            order=order,
            quantity = item['quantity']
        )
    return customer, order
