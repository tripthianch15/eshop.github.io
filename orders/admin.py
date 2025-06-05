from django.contrib import admin

# Register your models here.

from .models import Order
# Register your models here.
# Register your PaymentAdmin model with the admin
class OrderAdmin(admin.ModelAdmin):
    model = Order
    # Add or override any specific fields you want to show in the admin interface
    list_display = [ "order_id","order_date","buyer", "product","quantity","order_amount","order_status"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Restrict to the current user's orders if the user is a seller
        if request.user.is_superuser:
            return qs  # Superusers can see all orders
        return qs.filter(product__seller=request.user)  # Filter orders belonging to the logged-in seller


admin.site.register(Order,OrderAdmin)
