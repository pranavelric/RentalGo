from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import forms
from .forms import ProdForm, OrderForm, BuyForm
from .models import Product, Order, BuyOrder, Contact
import datetime
from django.views.decorators.csrf import csrf_exempt
from . import Checksum


# Create your views here.
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'

def home(request):
    products = Product.objects
    return render(request, 'products/home.html', {'products':products})

@login_required
def create(request):
    if request.method == 'POST':
        prod_form = ProdForm(request.POST,request.FILES)
        if prod_form.is_valid():
            product = prod_form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('/products/'+str(product.id))
        else:
            return render(request, 'products/create.html', {'prod_form':ProdForm})

    else:
        if request.user.profile.kyc_verified == "n":
            products = Product.objects
            return render(request, 'products/home.html', {'products':products, 'error':'Verify your kyc before posting an AD!'})

        else:
            prod_form = ProdForm
            return render(request, 'products/create.html', {'prod_form':prod_form})

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product':product})

@login_required
def new_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        # Take user to payment page
        if product.quantity == 0:
            return render(request, 'products/detail.html', {'product':product})
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.receiver = request.user
            order.sender = product.owner
            order.order_date = datetime.date.today()
            range = order.date_range.split(' - ')
            start = range[0].split('/')
            end = range[1].split('/')
            d1 = datetime.date( int(start[2]), int(start[1]), int(start[0]))
            d2 = datetime.date( int(end[2]), int(end[1]), int(end[0]))
            diff = d2-d1
            order.cost = (diff.days//30)*product.mprice + ((diff.days%30)//7)*product.wprice + (diff.days%7)*product.dprice
            if order.cost == 0:
                order_form = OrderForm
                return render(request, 'products/order.html', {'order_form':order_form, 'product':product, 'error':'Select two different dates'})
            order.save()
            product.quantity = product.quantity - 1
            product.save()
            param_dict = {
                'MID': 'WorldP64425807474247',
                'ORDER_ID': str(10000000000000000-order.id),
                'TXN_AMOUNT': str(order.cost),
                'CUST_ID': request.user.email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/products/payment_status/',
            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return render(request, 'products/paytm.html', {'param_dict': param_dict})
    else:
        if request.user.profile.kyc_verified == "n":
            return render(request, 'products/home.html', {'error':'Verify your kyc before ordering!'})
        else:
            order_form = OrderForm
            return render(request, 'products/order.html', {'order_form':order_form, 'product':product})

@csrf_exempt
def verify_payment(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            # print('order successful')
            pass
        else:
            order = get_object_or_404(Order, pk=100000000000000-int(response_dict['ORDERID']))
            product = get_object_or_404(Product, pk=order.product.id)
            product.quantity = product.quantity + 1
            product.save()
            order.delete()
        return render(request, 'products/paymentstatus.html', {'response': response_dict})
    else:
        redirect('home')

@login_required
def buy_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.available_for_selling == "n":
        redirect('home')
    if request.method == 'POST':
        # Take user to payment page
        if product.quantity == 0:
            return render(request, 'products/detail.html', {'product':product})
        form = BuyForm(request.POST)
        if form.is_valid():
            buyorder = form.save(commit=False)
            buyorder.product = product
            buyorder.receiver = request.user
            buyorder.sender = product.owner
            buyorder.order_date = datetime.date.today()
            buyorder.cost = product.sprice
            buyorder.save()
            product.quantity = product.quantity - 1
            product.save()
            param_dict = {
                'MID': 'WorldP64425807474247',
                'ORDER_ID': str(100000000000000-buyorder.id),
                'TXN_AMOUNT': str(buyorder.cost),
                'CUST_ID': request.user.email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/products/buy_payment_status/',
            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return render(request, 'products/paytm.html', {'param_dict': param_dict})
    else:
        if request.user.profile.kyc_verified == "n":
            return render(request, 'products/home.html', {'error':'Verify your kyc before ordering!'})
        else:
            buy_form = BuyForm
            return render(request, 'products/buyorder.html', {'buy_form':buy_form, 'product':product})

@csrf_exempt
def buy_payment(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            # print('order successful')
            pass
        else:
            buyorder = get_object_or_404(BuyOrder, pk=100000000000000-int(response_dict['ORDERID']))
            product = get_object_or_404(Product, pk=buyorder.product.id)
            product.quantity = product.quantity + 1
            product.save()
            buyorder.delete()
        return render(request, 'products/paymentstatus.html', {'response': response_dict})
    else:
        redirect('home')
def about(request):
    return render(request, 'about.html')

def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'contactus.html', {'thank': thank})

