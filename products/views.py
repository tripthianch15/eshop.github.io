
from .models import Product, Category,Cart, CartItem
from accounts.models import Seller, Buyer, CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse


from datetime import datetime, timedelta


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from .models import Product
from django.utils import timezone

def get_main_categories():
    categories = Category.objects.filter(parent_id=0)
    categories = {"main_categories":categories }
    return categories

def index_view(request):
    context = get_main_categories() 

    #return HttpResponse(crick_players)
    #print(context)
    site_title = get_site_title()
    #print(site_title)
    context.update(site_title)
    # if request.user.is_authenticated:
    cartdetails = get_cart_count(request)
    context.update(cartdetails)
    #print(context)
    return render(request,"products/index.html", context=context)

# Helper function to fetch categories and products
def get_categories_and_products(slug):
    context ={}
    if slug == "all":
        products = Product.objects.all()
        selected_category = slug
    else:
        #print("topic: ",topic)
        category = Category.objects.get(slug=slug)
        #print("category:",category)
        if category:
            products = Product.objects.filter(category=category.category_id)
            #print("products: ",products)
            selected_category = category.name
        else:
            products = Product.objects.all()
    
    context.update({'products':products,'selected_category':selected_category})
    #print(context)
    #categories = category_list_view()  
    categories = get_main_categories() 
    #print(categories)
    site_title = get_site_title()
    #print(site_title)
    context.update(categories)
    context.update(site_title)

    #print("context: ",context)
    return context

def marketplace_view(request, slug):
    context = get_categories_and_products(slug)
    #if request.user.is_authenticated:
    cartdetails = get_cart_count(request)
    context.update(cartdetails)
    delivery_date = get_delivery_date()
    context.update(delivery_date)
    return render(request, 'products/marketplace.html', context=context)

# def marketplace_view1(request, topic):
#     if topic == None:
#         products = Product.objects.all()
#     else:
#         category = Category.objects.get(slug=topic)
#         if category:
#             products = Product.objects.filter(category=category.category_id)
#         else:
#             products = Product.objects.all()
#     context = {'products':products}
#     #categories = category_list_view()  
#     categories = get_main_categories() 

#     site_title = get_site_title()
#     #print(site_title)
#     context.update(categories)
#     context.update(site_title)
#     print(context)
#     return render(request, 'products/marketplace.html', context=context)

def category_list_view():
    categories = Category.objects.all()  # Fetch all categories
    #return render(request, 'categories/category_list.html', {'categories': categories})
    return categories

def product_details_view(request, id):
    # Fetch the product by its ID or return a 404 error if not found
    product = get_object_or_404(Product, product_id=id)
    #product = Product.objects.get(product_id=id)
    #print("product details: ", product)
    # Pass the product details to the template
    context = {'product': product}
    categories = get_main_categories()
    context.update(categories)
    site_title = get_site_title()
    context.update(site_title)
    #if request.user.is_authenticated:
    cartdetails = get_cart_count(request)
    context.update(cartdetails)
    delivery_date = get_delivery_date()
    context.update(delivery_date)
    #print("delivery_date: ",delivery_date)
    #print("context: ",context)
    return render(request, 'products/product_details.html', context=context )

def add_to_cart_view1(request,id):
     product = get_object_or_404(Product, product_id=id)
     return HttpResponse(product)

def get_site_title():
    context = {"title":"Bharatha Online"}
    site_title = {"site_title":"Bharath Online Store - Organic Products, Groceries, Vegetables, Fruits, Staple food items raw rice, dal, Basamati rice, Dairy Products, A2 Milk, Ghee, Butter, Paneer, Cheese, Books, Books Religious, Rose flowers, Jaasmine flowers, Lotus flowers, Chrysanthemum flowers"}
    context.update(site_title)
    return context


#Ajax call, made from categories.html
def get_products(request):
    #print("get_products")
    slug = request.GET.get('slug')
    #print("slug : ",slug)
    context = get_categories_and_products(slug)
    #if request.user.is_authenticated:
    cartdetails = get_cart_count(request)
    context.update(cartdetails)
    delivery_date = get_delivery_date()
    context.update(delivery_date)
    #print(context)
    return render(request, 'products/products.html', context=context)

# Ajax call
def add_to_cart_view(request):
    if request.user.is_authenticated:
       
        product_id = request.GET.get('productId')
        print("Product ID: ", product_id)
        quantity = request.GET.get('quantity')
        print("Quantity: ",quantity)
        product = get_object_or_404(Product, product_id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if   item_created:
            print("cart_item.quantity-1: ",cart_item.quantity)
            cart_item.quantity = int(quantity)
            print("cart_item.quantity-2: ",cart_item.quantity)
        else:
            print("cart quanity before: ",cart_item.quantity)
            cart_item.quantity += int(quantity)
            print("cart quanity after: ",cart_item.quantity)
        cart_item.save()
        #return redirect('view_cart')
        #print("cart_item.quantity: ",cart_item.quantity)
        return HttpResponse(cart)

    else:
        return redirect('buyer_login')
        #return redirect('view_cart')

# Ajax call
def update_cart_view(request):
    if request.user.is_authenticated:
       
        product_id = request.GET.get('productId')
        print("Product ID: ", product_id)
        quantity = request.GET.get('quantity')
        print("Quantity: ",quantity)
        product = get_object_or_404(Product, product_id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if   item_created:
            cart_item.quantity = int(quantity)
            
        else:
            print("cart quanity before: ",cart_item.quantity)
            cart_item.quantity = int(quantity)
            print("cart quanity after: ",cart_item.quantity)
        cart_item.save()
        #return redirect('view_cart')
        print("cart_item.quantity: ",cart_item.quantity)
        return HttpResponse(cart)

    else:
        return redirect('buyer_login')
        #return redirect('view_cart')

@login_required
def cart_view(request):
    context = {}
    categories = get_main_categories()
    context.update(categories)
    site_title = get_site_title()
    context.update(site_title)
    if request.user.is_authenticated:
        cartdetails = get_cart_count(request)
        context.update(cartdetails)
        delivery_date = get_delivery_date()
        context.update(delivery_date)
        context.update({'currency': '₹'})
            #return render(request, 'products/cart.html', {'cart': cart,"cart_count":cartCount})
        return render(request, 'products/cart.html', context)
    else:
        return redirect('buyer_login')

@login_required
def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        return redirect('view_cart')
    else:
        return redirect('buyer_login')

def get_cart_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cartCount = cart.items.count
        return ({'cart': cart,"cart_count":cartCount})
    else:
        cartCount = 0
        return ({'cart': 0,"cart_count":cartCount})
    
# Helper functions

def get_delivery_date():
    # Calculate delivery date as current date plus 5 days
    delivery_date = datetime.now() + timedelta(days=5)
    
    # Get components of the date
    day_suffix = get_day_suffix(delivery_date.day)
    formatted_date = delivery_date.strftime(f"%a, %d{day_suffix} %b, %Y")
    
    # Return in a dictionary
    return {"delivery_date": formatted_date}

def get_day_suffix(day):
    # Determine the suffix for the day
    if 11 <= day <= 13:
        return "th"
    else:
        return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

@login_required
def dashboard_view(request):
    # Fetch data relevant to the seller
    if request.user.is_authenticated:
        if request.user.is_seller:

            seller = Seller.objects.get(username=request.user.username)
            print("seller: ", seller)
            products = Product.objects.filter(seller=seller)

            orders = Order.objects.filter(product__seller=seller)
            context = {
                'seller': seller,
                'products': products,
                'orders': orders,
            }
            # categories = get_main_categories() 
            # #print(categories)
        
            # context.update(categories)
            site_title = get_site_title()
            #print(site_title)
            context.update(site_title)
            #if request.user.is_authenticated:
            cartdetails = get_cart_count(request)
            context.update(cartdetails)
            return render(request, 'dashboard/dashboard.html', context)
        elif request.user.is_buyer:
                return redirect('/myorders/')
        elif request.user.is_admin:
            return redirect('/admin/')
    else:
        redirect('/')

    
    #return render(request, 'seller_dashboard/dashboard.html', context)
    

def my_products_view(request):
    
    seller = Seller.objects.get(username=request.user.username)
    print("seller: ", seller)
    products = Product.objects.filter(seller=seller)
    
    context = {
        'seller': seller,
        'products': products,
       
    }
    # categories = get_main_categories() 
    # #print(categories)
 
    # context.update(categories)
    site_title = get_site_title()
    #print(site_title)
    context.update(site_title)
            #if request.user.is_authenticated:
    cartdetails = get_cart_count(request)
    context.update(cartdetails)
    return render(request, 'seller_dashboard/myproducts.html', context)


# Example usage
# delivery_date_dict = get_delivery_date()
# print(delivery_date_dict)


def contact_us_view(request):
     site_title = get_site_title()
     #print(site_title)
  
     context = {'title':site_title}
     return render(request, "web-site/contact_us.html", context)

def about_us_view(request):
     site_title = get_site_title()
     #print(site_title)
     context = {'title':site_title}
     return render(request, "web-site/about_us.html", context)

def toc_view(request):
     return render(request, "web-site/terms_and_conditions.html")

def privacy_policy_view(request):
     return render(request, "web-site/privacy_policy.html")

def cancel_refund_view(request):
     return render(request, "web-site/cancellation_refund_policy.html")

def shipping_view(request):
     return render(request, "web-site/shipping_delivery_policy.html")
