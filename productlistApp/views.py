from django.shortcuts import render, redirect

# Create your views here.
from .models import user_list, product_item_list, add_to_cart_list
import random
import requests
from django.shortcuts import get_object_or_404
import os
import razorpay  # type: ignore
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from decimal import Decimal


# signup Function ===>
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        print("Signup --- > ")
        print("Username = ", username)
        print("Mobile Number = ", mobile)
        print("password1 = ", password1)
        print("password2 = ", password2)

        if user_list.objects.filter(Mobile = mobile).exists():
            return render(request, 'signup.html', {"error_mobile":"This mobile number is already registered. Please use a different number."})
        if password1==password2:

            otp = random.randint(1000, 9999)
            url = "https://2factor.in/API/V1/27ca43c3-a402-11ef-8b17-0200cd936042/SMS/{}/{}/".format(mobile,otp)
            print("URL = ", url)
            request.session['mobile'] = mobile
            request.session['otp'] = otp
            response = requests.get(url)

            if response.status_code == 200:
                database = user_list(Username=username, Mobile=mobile, Password1=password1, Password2=password2, Otp=otp, Verified=False, is_admin=False)
                database.save()
                return redirect('otp')
        else:
            return render(request, 'signup.html', {"error_password":"passwords do not matched. Please try again."})
        
    return render(request, 'signup.html')

# otp Function ===>
def otp(request):
    mobile = request.session.get('mobile')
    sessionotp = request.session.get('otp')

    if request.method == "POST":
        otp1 = request.POST.get('otp1')
        otp2 = request.POST.get('otp2')
        otp3 = request.POST.get('otp3')
        otp4 = request.POST.get('otp4')

        otp = otp1 + otp2 + otp3 + otp4
        print("Entered OTP = ",otp, "Session OTP = ", sessionotp)

        if otp == str(sessionotp):
            database = user_list.objects.get(Mobile=mobile)
            database.Verified = True
            database.save()
            return redirect('login')
    return render(request, 'otp.html')

# login Function ===>
def login(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        print("Login --- > ")
        print("Mobile Number = ", mobile)
        print("Password = ", password)
        
        user = user_list.objects.filter(Mobile=mobile, Password1=password, Verified=True).first()
        request.session['user_id'] = user.id
        if user:
            if user.is_admin:
                return redirect('productadmin')
            else :
                return redirect('productshow')
        else:
            return render(request, 'login.html', {"error_login":"Mobile number or password does not match, please enter the correct mobile number or password."})
        
    return render(request, 'login.html')

# productshow Function ===>
def productshow(request):
    # Current logged-in user ID
    user_id = request.session.get('user_id')
    if not user_id:
        # If no user logged in, redirect to login
        return redirect('login')

    # Fetch cart count for the logged-in user
    cart_count = add_to_cart_list.objects.filter(Userid=user_id).count()
    request.session['cart_count'] = cart_count  # Update session with cart count
    # Default: fetch all products
    selected_category = request.POST.get('Category', 'all')
    if selected_category == 'all':
        filtered_data = product_item_list.objects.all()
    else:
        # Filter based on selected category
        filtered_data = product_item_list.objects.filter(Category__iexact=selected_category)
    
    parsed_data = []
    for item in filtered_data:
        parsed_data.append({
            "id": item.id,
            "title": item.Title,
            "description": item.Description,
            "price": item.Price,
            "image": item.Images
        })
    
    print("Filtered Data = ", parsed_data)
    
    return render(request, 'productshow.html', {'product': parsed_data, 'cart_count': cart_count})

# productadmin Function ===>
def productadmin(request):
    response = requests.get("https://fakestoreapi.com/products")

    if response.status_code == 200:
        data = response.json()  # API thi data fetch karo
        
        for item in data:
            # Check karo ke item database ma already present che ke nai

            if not product_item_list.objects.filter(Title=item['title']).exists():
                response = requests.get(item['image'],stream=True)
                response.raise_for_status()
    
                img_url = os.path.basename(item['image'])
                print(img_url)
                media_path = os.path.join(settings.MEDIA_ROOT,'products_imges', img_url)
                
    
                with open(media_path, 'wb') as media_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        media_file.write(chunk)
                # Jo item nathi, to save karo
                print("Data successfully added to database!")
                database = product_item_list(
                    Title=item['title'],
                    Price=item['price'],
                    Description=item['description'],
                    Category=item['category'],
                    Images="products_imges/{}".format(img_url),
                    Rate=item['rating']['rate']
                )
                database.save()

        print("Dtabase in no changes!")
        
    else:
        print(f"Request failed with status code: {response.status_code}")
    
    # Database mathi data fetch karo ne pass karo template ma   
    products = product_item_list.objects.all()
    return render(request, 'productadmin.html', {'product': products})

# edit(productadmin) Function ===>
def edit(request, product_id):
    product = get_object_or_404(product_item_list, id=product_id) 
    if request.method == "POST":
        product.Title = request.POST.get('title')
        product.Price = request.POST.get('price')
        product.Description = request.POST.get('description')
        product.Category = request.POST.get('category')
        if 'images' in request.FILES and request.FILES['images']:
            product.Images = request.FILES['images']  # Update the image only if a new file is uploaded
        product.save()  
        return redirect('productadmin') 

    return render(request, 'edit_product.html', {'product': product})

# delete(productadmin) Function ===>
def delete(request, product_id):
    product = get_object_or_404(product_item_list, id=product_id) 
    product.delete() 
    return redirect('productadmin')

# add(productadmin) Function ===>
def add(request):
    if request.method == "POST":
        title = request.POST.get('title')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category = request.POST.get('category')
        images = request.FILES.get('images')  # Handle uploaded file

        product_item_list.objects.create(
            Title=title,
            Price=price,
            Description=description,
            Category=category,
            Images=images
        )

        return redirect('productadmin')  # Redirect to product list or homepage

    return render(request, 'addproduct.html')


# add_to_cart Function ===>
def add_to_cart(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        print("User-id = ", user_id)
        return redirect('login')  
    
    user = get_object_or_404(user_list, id=user_id)
    print(f"Current User: {user.Username} | Mobile: {user.Mobile}")

    product = product_item_list.objects.get(id=id)
    print(f"Add to Cart Product: {product.Title} | Price: {product.Price}")

    dict_product = {}

    if product.Images:  
        dict_product['Images'] = product.Images.url  

    dict_product = model_to_dict(product)
    dict_product['Price'] = float(dict_product['Price'])  # Convert Decimal to float
    dict_product['Images'] = product.Images.url if product.Images else ""

    json_product = json.dumps(dict_product)
    

    quantity = int(request.POST.get('quantity', 1))
    total_price = Decimal(product.Price) * quantity

     # Save to add_to_cart table
    add_to_cart_entry, created = add_to_cart_list.objects.get_or_create(
        Userid=user.id,
        Username=user.Username,
        Product_obj=json_product,
        defaults={  # Only used if creating a new entry
            'Quantity': quantity,
            'TotalPrice': total_price
        }
    )
    add_to_cart_entry.save()
    print("Check user.id = ", user.id)
    print(f"Product '{product.Title}' added to cart for user '{user.Username}'.")

    if not created:
        # update the quantity and total price
        add_to_cart_entry.Quantity = quantity
        add_to_cart_entry.TotalPrice = total_price
        add_to_cart_entry.save()

    cart_count = add_to_cart_list.objects.filter(Userid=user.id).count()
    request.session['cart_count'] = cart_count 
    return redirect('productshow')

# add_to_care_store Function ===>
def add_to_cart_store(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  
    if request.method == "POST":
        cart_item_id = request.POST.get('cart_item_id')  
        new_quantity = int(request.POST.get('quantity', 1))  
        print("New Quentity --- > ", new_quantity)
        
        cart_item = get_object_or_404(add_to_cart_list, id=cart_item_id, Userid=user_id)
        product_data = json.loads(cart_item.Product_obj)
        product_price = Decimal(product_data['Price'])  

        # Update total price based on new quantity
        cart_item.Quantity = new_quantity
        cart_item.TotalPrice = product_price * new_quantity
        cart_item.save()    

    cart_items = add_to_cart_list.objects.filter(Userid=user_id)

    subtotal = sum(item.TotalPrice for item in cart_items)

    parsed_cart_items = []
    for item in cart_items:
        product_data = json.loads(item.Product_obj) 
        product_data['cart_item_id'] = item.id 
        product_data['Quantity'] = item.Quantity 
        product_data['TotalPrice'] = item.TotalPrice
        parsed_cart_items.append(product_data)
    
    print("Cart Items:", parsed_cart_items)
    return render(request, 'add_to_cart_store.html', {'cart_items': parsed_cart_items, 'subtotal': subtotal})

def delete_cart_item(request):
    if request.method == "POST":
        cart_item_id = request.POST.get('cart_item_id')  # Cart item nu ID levo
        cart_item = get_object_or_404(add_to_cart_list, id=cart_item_id)
        cart_item.delete()
        return redirect('add_to_cart_store')
    return redirect('add_to_cart_store')


def checkout(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    # Get cart items for the user
    cart_items = add_to_cart_list.objects.filter(Userid=user_id)

    # Calculate subtotal
    subtotal = sum(item.TotalPrice for item in cart_items)

    # Static shipping cost (you can change as per your logic)
    shipping_cost = Decimal(9)

    # Calculate order total
    order_total = subtotal + shipping_cost

    # Prepare parsed cart items for the template
    parsed_cart_items = []
    for item in cart_items:
        product_data = json.loads(item.Product_obj)  # Parse product JSON
        product_data['cart_item_id'] = item.id
        product_data['Quantity'] = item.Quantity
        product_data['TotalPrice'] = item.TotalPrice
        parsed_cart_items.append(product_data)

    return render(request, 'checkout.html', {
        'cart_items': parsed_cart_items,  # Pass cart items to template
        'subtotal': subtotal,            # Pass subtotal
        'shipping_cost': shipping_cost,  # Pass shipping cost
        'order_total': order_total       # Pass order total
    })

from django.http import JsonResponse
from django.conf import settings

def create_payment(request):
    # Initialize Razorpay client
    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

    if request.method == "POST":

        email = request.POST.get("email", "")
        first_name = request.POST.get("first-name", "")
        last_name = request.POST.get("last-name", "")
        mobile = request.POST.get("mobile", "")
        address = request.POST.get("address", "")
        state = request.POST.get("state", "")
        pin_code = request.POST.get("pin-code", "")
        country = request.POST.get("country", "")

        print("Form Data:", email, first_name, last_name, mobile, address, state, pin_code, country)

        amount = 100  # Amount in INR * 100 (e.g., ₹100 = 10000 paise)

        try:
            print("First Name:", request.POST.get("first-name"))
            print("Last Name:", request.POST.get("last-name"))
            print("Email:", request.POST.get("email"))
            print("Mobile:", request.POST.get("mobile"))
            print("Amount = ", amount)
            # Create a Payment Link
            payment_link = razorpay_client.payment_link.create({
                "amount": amount,
                "currency": "INR",
                "accept_partial": False,
                "description": "Order Payment",
                "customer": {
                    "name": f"{first_name} {last_name}",
                    "email": email,
                    "contact": mobile,
                },
                "notify": {
                    "sms": True,
                    "email": True,
                },
                "callback_url": "https://127.0.0.1:8000/payment-success",
                "callback_method": "get"
            })
            print("Payment Link = ", payment_link)  # Debug response

            # Return Payment Link and QR Code URL
            return JsonResponse({
                'payment_link': payment_link['short_url'],  # Link for payment
                'qr_code': payment_link.get('short_url') + ".qr",         # URL to QR code image
            })

        except Exception as e:
            print(f"Error while creating payment link: {e}")
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method'})