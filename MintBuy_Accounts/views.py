# ---------------------------------------email--------------------------------------
import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect

from MintBuyApp.models import *
from .models import Profile,AboutUs,ContactUs


# ---------------------------------------email--------------------------------------

def home(request):
    car_pro = PRODUCT.objects.filter(carusel_prod=True)
    user = request.user
    if user.is_authenticated:
        cate = CATEGORIES.objects.all()
        len_cart = len(CART.objects.filter(user=user,purchased=False))
        cart_details = CART.objects.filter(user=user,purchased=False)[:2]
        all_cart = CART.objects.filter(user=user,purchased=False)
        subtotal = 0
        for i in all_cart:
            a = i.product.price * i.quantity
            subtotal += a

    return render(request, 'home.html', locals())


def Log_in(request):
    user = request.user
    if user.is_authenticated:
        cate = CATEGORIES.objects.all()
        len_cart = len(CART.objects.filter(user=user))
        cart_details = CART.objects.filter(user=user)[:2]
        all_cart = CART.objects.filter(user=user)
        subtotal = 0
        for i in all_cart:
            a = i.product.price * i.quantity
            subtotal += a

    if request.method == 'POST':
        name = request.POST.get('Name')
        password = request.POST.get('Pass')
        user = authenticate(username=name, password=password)
        if user:
            login(request, user)
            messages.success(request, "User logged in!")
            return redirect('home')
        else:
            messages.warning(request, "No User Found!")
            return redirect('Registration')

    return render(request, 'Accounts/Log_in.html', locals())


def log_out(request):
    logout(request)
    messages.warning(request, "User Logged Out!")
    return redirect('Log_in')


def Registration(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if password == password1:
            if User.objects.filter(Q(username=name) | Q(email=email)).exists():
                messages.warning(request, "Username or Email Already Taken!")
            else:
                user = User.objects.create_user(username=name, email=email, first_name=firstname, last_name=lastname,
                                                password=password)
                user.set_password(password)
                user.save()
                auth_token = str(uuid.uuid4())
                prof_obj = Profile.objects.create(user=user, auth_token=auth_token)
                prof_obj.save()
                send_mail_registration(email, auth_token)
                return render(request, 'Accounts/success.html')

        else:
            messages.warning(request, "Password Not Matched!")

    return render(request, 'Accounts/registration.html')


def send_mail_registration(email, token):
    subject = 'your verification link'
    massage = f' hi click this link to verify http://127.0.0.1:8000/verify/{token}'
    sender = settings.EMAIL_HOST_USER
    receive = [email]
    send_mail(subject, massage, sender, receive)


def verify(request, auth_token):
    prof = Profile.objects.filter(auth_token=auth_token).first()
    prof.is_verified = True

    user = prof.user

    login(request, user)
    return redirect('home')


def aboutus(request):
    about = AboutUs.objects.all()
    context = {
        'about': about,
    }

    return render(request, 'about-us.html', context)


def contact(request):
    user = request.user
    contact_us = ContactUs.objects.all()
    if user.is_authenticated:
        if request.method == 'POST' or request.method == 'post':
            user = user
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            massage = request.POST.get('massage')

            obj = UserMassage.objects.create(user=user,
                                             name=name,
                                             email=email,
                                             subject=subject,
                                             massage=massage,
                                             )
            obj.save()
            messages.success(request, f'Successfully Done')
            return redirect(request.META.get('HTTP_REFERER'))
        context = {
            'contact_us': contact_us,
        }
    return render(request, 'contact.html', locals())