from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser, Buyer, Seller
from products.models import Product, Inventory
#from payments.models import Payment
from datetime import datetime
#import random
import uuid
# Create your models here.

class Invoice(models.Model):
        class Meta:
            verbose_name = 'Invoice'
            verbose_name_plural = 'Invoices'
                         
class Order(models.Model):
        class Meta:
            verbose_name = 'Order'
            verbose_name_plural = 'Orders'
        YES = 'Y'
        NO = 'N'
        YesNoChoices = ((YES, 'Yes'),
                (NO, 'No'),)
        
        ADDRESS_TYPE = (
                ('Home', 'Home'),
                ('Office', 'Office'),
                ('Other', 'Other'),)
                
            
        ORDER_STATUS_CHOICES = (
                ('Placed', 'Placed'),
                ('Completed', 'Completed'),
                ('Incomplete', 'Incomplete'),
                ('Canceled', 'Canceled'),
                )
        
        DELIVERY_STATUS_CHOICES = (
                ('Notdelivered', 'Not Delivered'),
                ('Shipped', 'Shipped'),
                ('Delivered', 'Delivered'),
                ('Undelivered', 'Undelivered'),
                ('Door Closed', 'Door Closed'),
                ('Dispatched', 'Dispatched'),                
                ('Canceled', 'Canceled'),
                )
        buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
        inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE,null=True)
        
        quantity = models.PositiveIntegerField()
        
        order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')
        
        order_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
        order_date = models.DateTimeField(auto_now_add=True)
        date_created = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
        date_updated = models.DateTimeField(auto_now=True)    # Automatically set on update
        is_deleted = models.CharField(default=YES, blank = False, 
                                        choices=YesNoChoices,null = False,
                                        )
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        #inventory_id = models.ForeignKey(Inventory, on_delete=models.CASCADE)
        unit_rate = models.DecimalField(max_digits=20, decimal_places=2,null=True)
        order_amount = models.DecimalField(max_digits=20, decimal_places=2,null=True)
        delivery_charges =models.DecimalField(max_digits=20, decimal_places=2,null=True) # percentage
        discount_amount = models.DecimalField(max_digits=20, decimal_places=2,null=True)
        total_amount = models.DecimalField(max_digits=20, decimal_places=2,null=True)
        cgst =models.DecimalField(max_digits=10, decimal_places=2,null=True)
        sgst = models.DecimalField(max_digits=10, decimal_places=2,null=True)
        invoice_no =models.ForeignKey(Invoice, on_delete=models.CASCADE,null=True)
        delivery_date=models.DateTimeField(auto_now_add=True)
        delivery_status = models.CharField(default="Not Delivered", blank = False, 
                                        choices=DELIVERY_STATUS_CHOICES,null = False,
                                        ) # N - Means Not delivered, D- Means Dispached, Y - Means Delivered
        address_type = models.CharField(default="Home", blank = False, 
                                        choices=ADDRESS_TYPE,null = False,
                                        )
        delivery_address = models.CharField(default="", blank = True, null=True)
       

        # transaction_number from Payment
        transaction_id = models.CharField(max_length=255, blank=True, null=True)
      
        def __str__(self):
             return f"Payment for Order {self.order_id} - {self.order_status}"
      
        def save(self, *args, **kwargs):
        # Generate order_id if not already set
            if not self.order_id:
                #random_part = f"{random.randint(10000000, 99999999)}"
                #timestamp_part = datetime.now().strftime("%d%m%Y-%H-%M-%S")
                #timestamp_part = datetime.now().strftime("%d%m%Y%h%m%s")
                #self.order_id = f"{random_part}-{timestamp_part}"
                self.order_id = self.generate_order_id()
                timestamp_part = datetime.now().strftime("%d%m%Y-%H-%M-%S")
                self.order_date = timestamp_part
            super().save(*args, **kwargs)
    
        def generate_order_id(self):
            """Generate a unique and traceable order ID."""
            now = datetime.now()
            timestamp = now.strftime("%d%m%Y%H%M%S")  # e.g., 20250507143045
            unique_part = uuid.uuid4().hex[:6].upper()  # Shorten UUID for readability
            return f"ORD{timestamp}{unique_part}"


