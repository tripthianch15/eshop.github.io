from django.urls import path
from payments import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('payment/<int:order_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment/', views.initiate_payment, name='initiate_payment'),
    path('process_payment/<int:id>/', views.process_payment, name='process_payment'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]
