from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import HttpResponse
from django.contrib import messages,auth
from django.core.mail import send_mail
from .models import *
from .middlewares.auth import auth_middleware
from django.db import connections

cursor = connections['default'].cursor()
# Create your views here.
def index(request):
    if request.method == 'GET':
        quary = request.GET.get('search')
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()

        if quary:
            products = Product.get_products_by_quary(quary)
        data = {}
        data['products'] = products
        data['categories'] = categories
        return render(request, 'index.html', data)
    else:
        product = request.POST.get('product')
        cart = request.session.get('cart')
        remove = request.POST.get('remove')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1;
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        return redirect('home')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        postData = request.POST
        first = postData.get('firstname')
        last = postData.get('lastname')
        cont = postData.get('contact')
        email = postData.get('mail')
        password = postData.get('password')
        cpassword = postData.get('cpassword')

        # validation
        value = {
            'first_name': first,
            'last_name': last,
            'phone': cont,
            'email': email
        }
        error_msg = None
        if (not first):
            error_msg = "First Name Required!!"
        elif len(first) < 4:
            error_msg = "First name must be more 4 char"
        elif len(last) < 4:
            error_msg = "Last name must be more 4 char"
        elif len(cont) != 10:
            error_msg = "Phone number is not correct format"
        elif password != cpassword:
            error_msg = "Enter same password plz"
        elif customer.objects.filter(email=email).exists():
            error_msg = "Email is already registerd!!!!"

        # saving
        if not error_msg:
            cust = customer(first_name=first, last_name=last, phone=cont, email=email, password=make_password(password))
            cust.save();
            new_user_id = str(cust.id)
            link = "http://127.0.0.1:8000/activation/" + new_user_id + "/"
            message_text = "Click on the following link to complete your registration\n\n" + link
            # sending email
            send_mail(' Profile Activation', message_text, 'tshah8798@gmail.com',
                      [cust.email], fail_silently=False)
            messages.info(request, 'email link is being sent to your mail account')
            return redirect('signup')

        else:
            data = {
                'error': error_msg,
                'values': value
            }
            return render(request, 'signup.html', data)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        email = request.POST.get('mail')
        password = request.POST.get('password')
        cust = customer.get_customer_by_email(email)
        error_message = None
        if cust:
            flag = check_password(password, cust.password)
            if flag:
                request.session['customer'] = cust.id
                print(request.session['customer'])
                request.session['email'] = email
                
                return redirect('home')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'
        return render(request, 'login.html', {'error': error_message})

def activation(request, user_id):
    print("into activation")
    user = get_object_or_404(customer, pk=user_id)
    if user is not None:
        user.is_active = True
        user.save()
        return render(request,'login.html', context={
            'info_message': "Account successfully activated!"
        })

    else:
        return render(request, '/', context={
            'error_message': "Error with activation link!"
        })


def logout(request):
    request.session.clear()
    # auth.logout(request)
    return redirect('login')

@auth_middleware
def cart(request):
    if request.method == 'GET':
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print("$$$$$$$$$$$$$$$$$$$$$$",products)
        return render(request, 'cart.html', {'products': products})
    else:
        pass


def check_out(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        cust = request.session.get('customer')
        print(cust)
        Cart = request.session.get('cart')
        products = Product.get_products_by_id(list(Cart.keys()))
        #print(address, phone, cust, Cart, products)
        amt = []
        xyz = []
        print(Cart)
        print("###############",products)
        for product in products:
            order = Order(customer=customer(cust),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=Cart.get(str(product.id)))
            order.place_order()
            request.session['cart'] = {}
            a = Order.objects.raw('select id from store_order where id=(SELECT last_insert_rowid())')
            xyz.append(a[0].id)
            amt.append(product.price*Cart.get(str(product.id)))
        amts = sum(amt)
        or_num = OrderNumber(amount=amts)
        or_num.save()
        get_or = OrderNumber.objects.raw('select id from store_ordernumber where id=(SELECT last_insert_rowid())')
        for x in xyz:
            query = "Insert into store_ordernumber_order(ordernumber_id,order_id) values ("+str(get_or[0].id)+","+str(x)+")"
            cursor.execute(query)
        return redirect('cart')
   
@auth_middleware
def order(request):
    cust = request.session.get('customer')
    orders = Order.get_orders_by_customer(cust)
    return render(request, 'order.html', {'orders': orders})

def clear(request):
     request.session['cart'] = {}
     return redirect('home')
