from django.urls import path
from orders import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('create_order/', views.create_order, name='create_order'),
    path('myorders/', views.my_order_view, name='myorders'),
  
]
