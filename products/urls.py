from django.urls import path
from products import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   # path('marketplace/', views.marketplace_view, name='marketplace'),
    path('', views.index_view), 
    #path('marketplace/<str:topic>/',views.marketplace_view,name='marketplace'),
    path('marketplace/<str:slug>/',views.marketplace_view,name='marketplace'),
    path('categories/', views.category_list_view, name='category_list'),
    path('product_details/<int:id>/', views.product_details_view, name='product_details'),
    #path('add_to_cart/<int:id>/', views.add_to_cart_view, name='add_to_cart'),
    path('get-products/', views.get_products, name='get_products'),
    #path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    path('update_cart/', views.update_cart_view, name='update_cart'),
     
    path('cart/', views.cart_view, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('my_products/', views.my_products_view, name='my_products'),

    path('contact_us/',views.contact_us_view, name='contact_us'),
    path('about_us/',views.about_us_view, name='about_us'),
    path('terms_and_conditions/',views.toc_view, name='terms_and_conditions'),
    path('privacy_policy/',views.privacy_policy_view, name='privacy_policy'),
    path('cancellation_refund_policy/',views.cancel_refund_view, name='cancellation_refund_policy'),
    path('shipping_policy/',views.shipping_view, name='shipping_policy'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)