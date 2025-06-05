from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser
from orders.models import Order
from datetime import datetime
#import random
import uuid

# Create your models here.
class Payment(models.Model):

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    PAYMENT_STATUS_CHOICES = (
        ('Initiated', 'Initiated'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_payments')
    orders = models.ManyToManyField(Order, related_name='payments')
    #orders = models.CharField(max_length=1000, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2,default=0, null=True)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS_CHOICES, default='Initiated')
    transaction_id = models.CharField(default=0,max_length=255, unique=True, blank=True, null=True)
    gw_order_id = models.CharField(default=0,max_length=255,  blank=True, null=True)
    gw_payment_id = models.CharField(default=0,max_length=500, blank=True, null=True)
    gw_response = models.TextField(default='',null=True,blank=True)
    description = models.TextField(default='',null=True,blank=True)
    def save(self, *args, **kwargs):
        # Generate transaction_id if not already set
        if not self.transaction_id:
            #random_part = f"{random.randint(10000000, 99999999)}"
            #timestamp_part = datetime.now().strftime("%d%m%Y-%H-%M-%S")
            #self.transaction_id = f"{random_part}-{timestamp_part}"
            self.transaction_id = self.generate_transaction_id()
            self.payment_date = datetime.now().strftime("%d%m%Y-%H-%M-%S")
        # Calculate the total amount based on associated orders
        #self.amount = sum(order.order_amount for order in self.orders.all())
        super().save(*args, **kwargs)

    def generate_transaction_id(self):
        """Generate a unique and traceable order ID."""
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")  # e.g., 20250507143045
        unique_part = uuid.uuid4().hex[:6].upper()  # Shorten UUID for readability
        return f"TXN{self.user.id}{timestamp}{unique_part}"

