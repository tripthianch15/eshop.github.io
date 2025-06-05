
from .models import Product

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse


from datetime import datetime, timedelta


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from products.models import Product, Cart, CartItem

from django.utils import timezone

def get_site_title():
    return {"site_title":"Bharath Store - Organic Products, Groceries, Vegetables, Fruits, Staple food items raw rice, dal, Basamati rice, Dairy Products, A2 Milk, Ghee, Butter, Paneer, Cheese"}

# Create your views here.
# views.py
@login_required
def my_order_view(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        
        'orders': orders
    }
    site_title = get_site_title()
    #print(site_title)
    context.update(site_title)
            #if request.user.is_authenticated:
    cartdetails = get_cart_count(request)
    context.update(cartdetails)
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def checkout(request):
    #cart_items = request.session.get('cart', {})
    #cart_items = CartItem.objects.filter(request.user)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    print("cart_items: ",cart_items)

    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('cart_view')  # Redirect to the cart page if the cart is empty

    # Assuming the cart is a dictionary with product IDs as keys and quantities as values
    products = []
    orders = []
    total_price = 0
    #for product_id, quantity in cart_items.items():
    #for product_id, quantity in cart_items:
    total_selling_amount = 0.0
    total_order_amount = 0.0
    total_delivery_charges = 0.0
    total_discount = 0.0
    for item in cart_items:
        #product = Product.objects.get(id=item.product.product_id)
        print("cart item: ", item)
        delivery_charges = (item.quantity * item.product.selling_price*item.product.delivery_charges/100)
        sub_total = (item.quantity * item.product.selling_price) + delivery_charges
        total_order_amount = float(total_order_amount) + float(sub_total)
        currency = item.product.currency
        total_selling_amount = float(total_selling_amount) + float((item.quantity * item.product.selling_price))
        total_delivery_charges = float(total_delivery_charges) + float(delivery_charges)
        products.append({            
            'product': item.product,
            'quantity': item.quantity*item.product.quantity,
            'subtotal': sub_total,
            'delivery_charges':delivery_charges
        })
        order = create_order(request,item)
        orders.append({'order':order})
        #total_price += item.product.selling_price * item.product.quantity
    ###########
    
    # #########    
    
    print("total_order_amount: ",total_order_amount)
    context = {
        'products': products,
        'total_order_amount': total_order_amount,
        'total_delivery_charges':total_delivery_charges,
        'total_selling_amount': total_selling_amount,
        'orders': orders,
        'currency': currency
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_confirmation(request):
    return render(request, 'orders/order_confirmation.html')

@login_required
def create_order(request, item):
    # Assume the user has items in a cart and we're processing the checkout
    #cart_items = request.session.get('cart', {})  # Get cart items from session (or use a Cart model)
    if item.product.available_stock < item.product.quantity:
            msg = f"Not enough stock for {item.product.product_name}. Available: {item.product.available_stock}"
            messages.error(request, msg)
            return redirect('/view_cart/')

        # Create order instance
    delivery_charges = item.product.selling_price * item.quantity * item.product.delivery_charges / 100
    total_order_amount = item.product.selling_price * item.quantity + delivery_charges
    order = Order.objects.create(
                buyer=request.user,
                product=item.product,
                quantity=item.product.quantity * item.quantity,
                unit_rate = item.product.selling_price,
                #selling_price = item.product.selling_price,
                
                delivery_charges = delivery_charges,
                discount_amount = item.product.discount,
                order_date=timezone.now(),
                total_amount = total_order_amount,
                order_status='Placed',
                order_amount=item.product.selling_price * item.quantity            
            )
        
    # Decrease stock after order is created
    item.product.available_stock -= item.product.quantity
    item.product.save()
    return Order


