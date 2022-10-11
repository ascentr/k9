# from email.policy import default
# from io import open_code
# from itertools import product
# from pyexpat import model
# from statistics import mode
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField( User, null=True, blank=True, on_delete=models.CASCADE, related_name="customer")
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name


class Brand(models.Model):
    brand = models.CharField(max_length=200, blank=True)
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    weight= models.PositiveIntegerField(default=454)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="product_brand", blank=True, default=1)
    flavour = models.CharField(max_length=200, blank=True)
    discription = models.TextField(default='')
    image = models.ImageField(null=True, blank=True)

    # multibuy = models.BooleanField(default=True)
    # multibuy_name = models.CharField(max_length=200,  default='')
    # multibuy_quantity = models.PositiveIntegerField(default=8, blank=True, null=True)
    # multibuy_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

# class Multibuy(models.Model):
#     name = models.CharField(max_length=200, default='Multibuy')
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="multibuy_brand", blank=True, default=1)
#     product = models.ForeignKey(Product,  on_delete=models.SET_NULL, null=True)
#     max_items = models.IntegerField(default=8, null=True, blank=True)
#     price = models.DecimalField(max_digits=8, decimal_places=2)


class Bundle(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="bundle_brand", blank=True, default=1)
    product = models.ForeignKey(Product,  on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    max_items = models.IntegerField(default=8, null=True, blank=True)


class Order(models.Model):
    customer = models.ForeignKey( Customer,  on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property 
    def shipping(self):
        shipping = True
        orderitems = self.orderitem_set.all()

        # for i in orderitems:
        #     if i.product.digital == False:
        #         shipping = True                
        return shipping


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product,  on_delete=models.SET_NULL, null=True)
    order =   models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	postcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)


'''

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    county = models.CharField(max_length=200, null=False) 
    postcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
'''

