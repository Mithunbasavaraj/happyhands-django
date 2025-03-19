from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.contrib import messages
from . models import product,cart,order
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
import shortuuid
from cryptography.hazmat.primitives import hashes
from django.views.decorators.csrf import csrf_exempt
from cryptography.hazmat.backends import default_backend
import json 
import base64
import requests





def home(request):
    return render(request, "index.html")

def products(request):
    post=product.objects.all()
    search_post = request.GET.get('search')
    if search_post:
     post = product.objects.filter(Q(product_name__icontains=search_post) |Q(key_words__icontains=search_post) | Q(product_description__icontains=search_post) | Q(juice_type__icontains=search_post) | Q(category__icontains=search_post) | Q(slug__icontains=search_post)| Q(quantity__icontains=search_post)).order_by("-id") 
    print(post)
    content={
       "post":post
    }
    return render(request, "products.html",content)

def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        message=request.POST.get("message")
        Subject=request.POST.get("subject")
        print(name,Subject,phone,email,message)
        subject = f'Contact Message from {name}  {Subject}'
        message = f'Message from {name} , \n{message}\n{phone}\n{email}\n{Subject}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]
        send_mail( subject, message, email_from, recipient_list )
        messages.success(request, "Thank You We Will Contact You Soon!")
    return render(request, "contact.html")

def as_view(request):
    logout(request)
    messages.success(request, "Logout Success")
    return redirect("base:login")

def authView(request):
 if request.method == "POST":
  form = RegistrationForm(request.POST or None)
  if form.is_valid():
   form.save()
   messages.success(request, "Register Success")
   return redirect("base:login")
 else:
  form = RegistrationForm()
 return render(request, "registration/signup.html", {"form": form})


# product details
def product_details(request,slug,pk):
    post=product.objects.get(id=pk)
    re_post=product.objects.filter(juice_type=post.juice_type)
    content={
       "post":post,
       "re_post":re_post,
    }
    return render(request, "product-details.html",content)



# add to cart
@login_required
def add_to_cart(request,pk):
    pro=product.objects.get(id=pk) 
    user=request.user
    unit_qty=int(request.POST.get("unit_qty"))
    amount=(pro.price*unit_qty)
    my_query=cart(user=user,product=pro,amount=amount,unit_qty=unit_qty)
    my_query.save()
    messages.success(request, "Added Success")
    return redirect("base:cart_page")


# add to cart
def cart_page(request):
    post=cart.objects.filter(user=request.user)
    total_qty=post.count()
    sub_total = sum(post.values_list("amount",flat=True))
    if post.exists():
       cart_exists=True
    else:
       cart_exists=False
    content={
       "post":post,
       "total_qty":total_qty,
       "sub_total":sub_total,
       "cart_exists":cart_exists
    }
    return render(request, "cart-page.html",content)


# remove from cart
def remove_from_cart(request, pk):
    cart_item = cart.objects.get(id=pk)
    cart_item.delete()
    messages.success(request, "Product Deleted")
    return redirect("base:cart_page")

    

# aty add from cart
def qty_add(request ,pk):
    qty_input=int(request.POST.get("qty_input"))
    post=cart.objects.get(id=pk)
    qty_input=qty_input+1
    post.amount=qty_input*post.product.price
    post.unit_qty=qty_input
    post.save()
    messages.success(request, "Cart Updated")
    return redirect("base:cart_page")

# aty sub from cart
def qty_sub(request,pk):
    qty_input=int(request.POST.get("qty_input"))
    post=cart.objects.get(id=pk)
    if qty_input>1:
        qty_input=qty_input-1
        post.amount=qty_input*post.product.price
        post.unit_qty=qty_input
        post.save()
        messages.success(request, "Cart Updated")
    else:
       post.delete()
       messages.success(request, "Product Deleted")
    return redirect("base:cart_page")


# profile
def profile(request):
    all_orders=order.objects.filter(user=request.user).order_by('-id')
    content={
       "all_orders":all_orders,  
    }
    return render(request, "profile.html",content)

# order_details
def order_details(request, pk):
    return render(request, "order-details.html")

# admin_order_view
def admin_order_view(request):
    all_orders=order.objects.all().order_by('-id')
    content={
       "all_orders":all_orders,    
    }
    return render(request, "order-view.html",content)

# checkout
def checkout(request):
    return render(request, "checkout.html")

# payment

def calculate_sha256_string(input_string):
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    sha256.update(input_string.encode('utf-8'))
    return sha256.finalize().hex()
def base64_encode(input_dict):
    json_data = json.dumps(input_dict)
    data_bytes = json_data.encode('utf-8')
    return base64.b64encode(data_bytes).decode('utf-8')

@login_required
def pay(request):
 cart_items = cart.objects.filter(user=request.user)
 total_price = sum(cart_items.values_list("final_price",flat=True))
 if request.method=="POST":
    uid = shortuuid.uuid()
    total_price=request.POST.get("total_price")
    j_cart_product=request.POST.get("j_cart_product")
    name=request.POST.get("name")
    phone_number=request.POST.get("phone_number")
    email=request.POST.get("email")
    house_no=request.POST.get("house_no")
    area=request.POST.get("area")
    city=request.POST.get("city")
    state=request.POST.get("state")
    pin_code=request.POST.get("pin_code")
    landmark=request.POST.get("landmark")
    order_status="PENDING"
    my_query=order(user=request.user,total_price=total_price,payment_status=order_status,order_id=uid,j_cart_product=j_cart_product,name=name,phone=phone_number,email=email,house_no=house_no,area=area,city=city,state=state,pin_code=pin_code,landmark=landmark)
    my_query.save()
    MAINPAYLOAD = {
        "merchantId": "PGTESTPAYUAT92",
        "merchantTransactionId": uid,
        "merchantUserId": "MUID123",
        "amount": 100,
        "redirectUrl": "http://127.0.0.1:8000/return-to-me/",
        "redirectMode": "POST",
        "callbackUrl": "http://127.0.0.1:8000/return-to-me/",
        "mobileNumber": phone_number,
        "paymentInstrument": {
            "type": "PAY_PAGE"
        }
    }
    # SETTING
    INDEX = "1"
    ENDPOINT = "/pg/v1/pay"
    SALTKEY = "2ecdb483-6888-4a97-ab3c-6725b15a034f"
    
    base64String = base64_encode(MAINPAYLOAD)
    mainString = base64String + ENDPOINT + SALTKEY;
    sha256Val = calculate_sha256_string(mainString)
    checkSum = sha256Val + '###' + INDEX;
    headers = {
        'Content-Type': 'application/json',
        'X-VERIFY': checkSum,
        'accept': 'application/json',
    }
    json_data = {
        'request': base64String,
    }
    response = requests.post('https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay', headers=headers, json=json_data)
    responseData = response.json();
    payurl =responseData['data']['instrumentResponse']['redirectInfo']['url']
    return  render(request, 'pay.html', {'outputurl': payurl})

@csrf_exempt    
def payment_return(request):
    INDEX = "1"
    SALTKEY = "2ecdb483-6888-4a97-ab3c-6725b15a034f"
    form_data = request.POST
    form_data_dict = dict(form_data)
    transaction_id = form_data.get('transactionId', None)
    if transaction_id:
        request_url = 'https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/PGTESTPAYUAT92/' + transaction_id;
        sha256_Pay_load_String = '/pg/v1/status/PGTESTPAYUAT92/' + transaction_id + SALTKEY;
        sha256_val = calculate_sha256_string(sha256_Pay_load_String);
        checksum = sha256_val + '###' + INDEX;
        # Payload Send
        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': checksum,
            'X-MERCHANT-ID': "PGTESTPAYUAT92",
            'accept': 'application/json',
        }
        response = requests.get(request_url, headers=headers)
        json_data=json.loads(response.text)
        code_data=json_data["code"]
        m_transaction_id=json_data["data"]["merchantTransactionId"]
        transaction_id=json_data["data"]["transactionId"]
        if code_data=="PAYMENT_SUCCESS":
         return render(request, 'return.html', {'m_transaction_id': m_transaction_id,'transaction_id':transaction_id})
        else:
         return render(request, 'failed.html', {})

def order_success(request):
   m_transaction_id=request.GET.get("m_transaction_id")
   p_transaction_id=request.GET.get("transaction_id")
   order_update=order.objects.get(order_id=m_transaction_id)
   order_update.transaction_id=p_transaction_id
   order_update.payment_status="PAID"
   order_update.Order_status="Order placed"
   order_update.save()
   user=request.user
   cart_delete=cart.objects.filter(user=user)
   print(order_update.email)
   for c in cart_delete:
    c.delete() 

   subject = f'  Order Placed Successful - OID{order_update.pk} '
   message = f'Hi {user.first_name}, \nThank you for trusting us! We are thrilled to confirm that your order, OID{order_update.pk}, has been received and is being processed. \nTrack Order -  http://127.0.0.1:8000/conformed-orders/details/{order_update.pk} \n Warm Regards, \n Happy Hands'
   email_from = settings.EMAIL_HOST_USER
   recipient_list = [user.email, order_update.email,"3dfloorcoating@gmail.com"]
   send_mail( subject, message, email_from, recipient_list )
   return redirect("base:profile")
#    return render(request, 'order-success.html', {})


