from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import *
from sslcommerz_lib import SSLCOMMERZ
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def product(request, id):
    user = request.user
    if user.is_authenticated:
        cate = CATEGORIES.objects.all()
        len_cart = len(CART.objects.filter(user=user, purchased=False))
        cart_details = CART.objects.filter(user=user, purchased=False)[:2]
        all_cart = CART.objects.filter(user=user, purchased=False)
        subtotal = 0
        for i in all_cart:
            a = i.product.price * i.quantity
            subtotal += a

    prod = PRODUCT.objects.filter(category=id)
    return render(request, 'shop/all_product.html', locals())


def single_product(request, id):
    user = request.user
    if user.is_authenticated:
        len_cart = len(CART.objects.filter(user=user, purchased=False))
        cart_details = CART.objects.filter(user=user, purchased=False)[:2]
        all_cart = CART.objects.filter(user=user, purchased=False)
        subtotal = 0
        for i in all_cart:
            a = i.product.price * i.quantity
            subtotal += a

        sing_prod = PRODUCT.objects.get(id=id)

    return render(request, 'shop/single_product_page.html', locals())


def addtoCart(request, id):
    prod = PRODUCT.objects.get(id=id)
    user = request.user
    if prod:
        if user.is_authenticated:
            try:
                cart = CART.objects.get(Q(user=user) & Q(product=prod) & Q(purchased=False))
                if cart:
                    cart.quantity += 1
                    cart.save()
                    return redirect(request.META['HTTP_REFERER'])
            except:
                new_cart = CART.objects.create(user=user, purchased=False, product=prod)
                new_cart.save()
                return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect('Log_in')
    return redirect(request.META['HTTP_REFERER'])


def remove_cart(request, id):
    cart = CART.objects.get(id=id,purchased=False)
    cart.delete()
    return redirect(request.META['HTTP_REFERER'])


def cart(request):
    user = request.user
    if user.is_authenticated:
        len_cart = len(CART.objects.filter(user=user,purchased=False))
        cart_details = CART.objects.filter(user=user,purchased=False)[:2]
        all_cart = CART.objects.filter(user=user,purchased=False)
        subtotal = 0
        for i in all_cart:
            a = i.product.price * i.quantity
            subtotal += a

    return render(request, 'shop/shopping-cart.html', locals())


def checkout(request):
    user = request.user
    len_cart = len(CART.objects.filter(user=user,purchased=False))
    cart_details = CART.objects.filter(user=user,purchased=False)[:2]
    all_cart = CART.objects.filter(user=user,purchased=False)
    subtotal = 0
    for i in all_cart:
        a = i.product.price * i.quantity
        subtotal += a
    total = subtotal
    try:
        if all_cart:
            for i in all_cart:
                if i.quantity > 1:
                    delivery_charge = 0
                    total += delivery_charge

                elif len_cart > 1:
                    delivery_charge = 0
                    total += delivery_charge
                else:
                    if request.method == 'POST':
                        del_cost = request.POST['deliver']

                        if del_cost == '1':
                            delivery_charge = 70
                            total += delivery_charge
                        else:
                            delivery_charge = 100
                            total += delivery_charge
    except:
        messages.warning(request, "Choose delivery option!")
        return redirect(request.META['HTTP_REFERER'])

    return render(request, 'shop/checkout.html', locals())


def plus_cart(request, id):
    prod = PRODUCT.objects.get(id=id)
    user = request.user
    if prod:
        if user.is_authenticated:
            cart = CART.objects.get(user=user, product=prod,purchased=False)
            if cart:
                cart.quantity += 1
                cart.save()
                return redirect(request.META['HTTP_REFERER'])

    return redirect(request.META['HTTP_REFERER'])


def minus_cart(request, id):
    user = request.user
    prod = PRODUCT.objects.get(id=id)
    if user.is_authenticated:
        cart = CART.objects.get(user=user, product=prod,purchased=False)
        if cart:
            cart.quantity -= 1
            if cart.quantity < 1:
                cart.delete()
                return redirect(request.META['HTTP_REFERER'])
            cart.save()
            return redirect(request.META['HTTP_REFERER'])

    return redirect(request.META['HTTP_REFERER'])


def sslcomerz(request):
    user = request.user
    len_cart = len(CART.objects.filter(user=user,purchased=False))
    cart_details = CART.objects.filter(user=user,purchased=False)[:2]
    all_cart = CART.objects.filter(user=user,purchased=False)
    subtotal = 0
    for i in all_cart:
        a = i.product.price * i.quantity
        subtotal += a
    total = subtotal
    if request.method == 'POST':
        del_cost = request.POST['deliver']

        if del_cost == '2':
            sslcz = SSLCOMMERZ({'store_id': 'niyam6412dc52e1e89', 'store_pass': 'niyam6412dc52e1e89@ssl', 'issandbox': True})
            data = {
                'total_amount': total,
                'currency': "BDT",
                'tran_id': "tran_12345",
                'success_url': "http://127.0.0.1:8000/MintBuyApp/success/",
                # if transaction is succesful, user will be redirected here
                'fail_url': "http://127.0.0.1:8000/MintBuyApp/fail/",  # if transaction is failed, user will be redirected here
                # 'cancel_url': "http://127.0.0.1:8000/payment-cancelled",
                # after user cancels the transaction, will be redirected here
                'emi_option': "0",
                'cus_name': "test",
                'cus_email': "test@test.com",
                'cus_phone': "01700000000",
                'cus_add1': "customer address",
                'cus_city': "Dhaka",
                'cus_country': "Bangladesh",
                'shipping_method': "NO",
                'multi_card_name': "",
                'num_of_item': 1,
                'product_name': "Test",
                'product_category': "Test Category",
                'product_profile': "general",
            }

            response = sslcz.createSession(data)
            return redirect(response['GatewayPageURL'])
        else:
            return render(request, 'shop/success.html')

@csrf_exempt
def success(request):
    cart = CART.objects.filter(purchased=False)

    for cart_item in cart:
        cart_item.purchased = True
        cart_item.save()
    return render (request, 'shop/success.html')

@csrf_exempt
def fail(request):
    return render (request, 'shop/fail.html')