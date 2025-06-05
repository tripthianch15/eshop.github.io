from django.db import models
class Product(models.Model):
    
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    #product_owner = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='products/product_images/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)