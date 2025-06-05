from django.contrib import admin
from .models import Payment

# Register your models here.
# Register your PaymentAdmin model with the admin
class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    # Add or override any specific fields you want to show in the admin interface
    list_display = ['user' ,'transaction_id',"amount", "payment_date", "payment_status"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Restrict to the current user's payments if the user is a seller
        if request.user.is_superuser:
            return qs  # Superusers can see all payments
        return qs.filter(user=request.user)  # Filter products belonging to the logged-in seller

admin.site.register(Payment,PaymentAdmin)
