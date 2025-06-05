# accounts/admin.py
from django.contrib import admin
from .models import CustomUser, Buyer, Seller, UserKYC

class CustomUserAdmin(admin.ModelAdmin):
    # list_display = ['username', 'first_name','last_name','contact_number','email','is_seller', 'is_buyer','deleted','email_verified', 'phone_verified']

    # search_fields = ['deleted']
    list_display = ('username','email', 'contact_number', 'user_type', 'is_email_verified', 'is_phone_verified', 'is_active', 'is_staff')
    list_filter = ('user_type', 'is_email_verified', 'is_phone_verified', 'is_active')
    search_fields = ('email', 'contact_number')

    ordering = ('-date_joined',)

    # fieldsets = (
    #     (None, {'fields': ('email', 'password', 'contact_number',)}),
    #     ('Roles', {'fields': ('user_type',)}),
    #     ('Verification', {'fields': ('is_email_verified', 'is_phone_verified',)}),
    #     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
    # )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'phone_number', 'password1', 'password2'),
    #     }),
    # )


class BuyerAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active', 'is_deleted']
    search_fields = ['user__username']

class SellerAdmin(admin.ModelAdmin):
    list_display = ['user', 'store_name', 'store_approved']
    search_fields = ['store_name']

class UserKYCAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserKYC, UserKYCAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Seller, SellerAdmin)

