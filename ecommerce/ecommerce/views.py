from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import Contacts_form
from django.core.mail import send_mail
from django.conf import settings
from store.utils import cartData, cookieCart, guestOrder



def index(request):
    if cartData:
        data = cartData(request)
        cartItems = data['cartItems']
        context = {'cartItems':cartItems }
    else:
       
        context = {}
        
    return render(request, 'index.html', context)


def benefits(request):
    return render(request, 'benefits.html')


def contactsView(request):
    if request.method == 'GET':
        form = Contacts_form()

    else:
        form = Contacts_form(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            message = from_email + ' ' + message

            try:
                send_mail(subject, message, from_email, ['786dev2020@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success/')

    return render(request, "contacts.html", {'form':form})


def successView(request):
#    return HttpResponse('Success ! Thanks for your message')
    return render(request, "success.html")