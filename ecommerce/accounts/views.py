from http.client import HTTPResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms
from  store.utils import cookieCart, cartData, guestOrder
from django.conf import settings
from store.models import Customer

def signup(request):
    form = forms.UserCreateForm

#display cartinfo for the auth pages

    data = cartData(request)
    cartItems = data['cartItems']

    if request.method =="POST":
        form = forms.UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()

            Customer.objects.create(
                user = new_user,
                name = new_user.username,
                email = new_user.email
            )    


            messages.info(request, 'Thanks for Registering')

            new_user = authenticate(
                username = form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                )
            login(request, new_user)

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('index')

    context = { 'form' : form , 'data': data, 'cartItems':cartItems}
    return render( request, 'accounts/signup.html',  context)