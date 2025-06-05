from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('buyer_signup/', views.buyer_signup_view, name='buyer_registration'),
    path('buyer_login/', views.buyer_login_view, name='buyer_login'),
    # To be updated
    path('seller_login/', views.seller_login_view, name='seller_login'),
    path('seller/registration/', views.seller_registration_view, name='seller_registration'),
    
    #path('staff_login/', views.staff_login_view, name='staff_login'),
    path('buyer_shipping_address/', views.shipping_address_view),
    path('buyer/', views.buyer_view, name="buyer"),
    path('buyer_change_password/', views.buyer_change_password_view, name='change_password'),
    path("buyer_logout/", views.logout_view, name="logout"),

   #path('forgot_password',views.forgot_password_view, name='forgot_password'),
   #path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
   path('confirm_otp/',views.confirm_otp_view, name='confirm_otp'),
   path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]