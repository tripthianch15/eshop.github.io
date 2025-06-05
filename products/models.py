from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser, Buyer, Seller
from datetime import datetime
import random
# Create your models here.

# from seller.models import Seller
# models.py
  
    
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  # Allow blank initially so it can be generated
    description = models.TextField(blank=True, null=True)
    category_image = models.ImageField(upload_to='products/category_images/',default='')
    parent_id = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it doesn't exist
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    ml = 'ML'     
    litre = 'Litre'
    gram = 'Gram'
    kg = 'K.G.'
    number = 'Nos.'
    NA = "NA"

    QTY = (
            (litre,"Litre"),
            (ml,"ml"),
            (gram,"Gram"),
            (kg,"K.G."), 
            (number,"Nos."),
            (NA, "NA"),)
    
    INR = '₹' 
    USD = '$'
    #Euro = ''

    CURRENCY = ((INR,"₹"),
                (USD,"$"),)
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    #product_owner = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='products/product_images/')
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=20, decimal_places=2)
    available_stock = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    date_updated = models.DateTimeField(auto_now=True)    # Automatically set on update
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    currency = models.CharField(max_length=1,default=INR, blank = True, 
                                        choices=CURRENCY, null = False
                                        ) 
    quantity =  models.IntegerField(default=5) 
    cgst = models.DecimalField(default=0,max_digits=10, decimal_places=2)   # Percentage 
    sgst = models.DecimalField(default=0,max_digits=10, decimal_places=2)   # Percentage 
    delivery_charges = models.DecimalField(default=0,max_digits=10, decimal_places=2)   # Percentage 
    measurement = models.CharField(max_length=10,default=kg, blank = True, 
                                       choices=QTY, null = False) 
    
    def __str__(self):
        return self.product_name


# Cart Model
class Cart(models.Model):
    
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total_delivery_charges(self):
        return sum(item.get_total_delivery_charges() for item in self.items.all())
    
    def get_total_cart_discount(self):
        return sum(item.get_total_discount() for item in self.items.all())
    
    def get_total_order_amount(self):
        return sum(item.get_total_price() + item.get_total_delivery_charges() for item in self.items.all())
    def __str__(self):
        return self.user.username


# Cart Item Model
class CartItem(models.Model):
    class Meta:
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return (self.product.selling_price * self.quantity)
    
    def get_total_delivery_charges(self):
        return ((self.product.selling_price * self.quantity)*(self.product.delivery_charges)/100)
    
    def get_total_discount(self):
        price = self.product.price * self.quantity
        selling_price = self.product.selling_price * self.quantity
        discount = price - selling_price
        return discount

    def get_total_quantity(self):
        return self.product.quantity * self.quantity
    
class Inventory(models.Model):
    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'
    ml = 'ML'     
    litre = 'Litre'
    gram = 'Gram'
    kg = 'K.G.'
    number = 'Nos.'
    NA = "NA"

    QTY = (
         (litre,"Litre"),
         (ml,"ml"),
         (gram,"Gram"),
         (kg,"K.G."), 
         (number,"Nos."),
         (NA, "NA"),)
        
    INR = '₹' 
    USD = '$'
    #Euro = ''

    CURRENCY = ((INR,"₹"),
               (USD,"$"),)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_stock = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    date_updated = models.DateTimeField(auto_now=True)    # Automatically set on update
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    currency = models.CharField(max_length=1,default=INR, blank = True, 
                                        choices=CURRENCY, null = False
                                        ) 
    quantity =  models.IntegerField(default=5) 
        
    measurement = models.CharField(max_length=10,default=kg, blank = True, 
                                        choices=QTY, null = False) 
    
    def __str__(self):
          return self.product.product_name
    
    