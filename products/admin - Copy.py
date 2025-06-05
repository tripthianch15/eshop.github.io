from django.contrib import admin

from .models import Product, Category,Cart,CartItem
# Register your models here.
# Register your CustomUser model with the admin
class ProductAdmin(admin.ModelAdmin):
    model = Product
    # Add or override any specific fields you want to show in the admin interface
    list_display = [ 'product_name',"product_id","category","seller", 'price', 'discount','selling_price', 'available_stock']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Restrict to the current user's products if the user is a seller
        if request.user.is_superuser:
            return qs  # Superusers can see all products
        return qs.filter(seller=request.user)  # Filter products belonging to the logged-in seller

class CartAdmin(admin.ModelAdmin):
    model = Cart
    # Add or override any specific fields you want to show in the admin interface
    list_display = ["created_at", "user"]


class CartItemAdmin(admin.ModelAdmin):
    model = CartItem
    # Add or override any specific fields you want to show in the admin interface
    list_display = ["cart","product","quantity"]

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
