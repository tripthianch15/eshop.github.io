from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path('', views.index_view), 
     path('marketplace/<str:slug>/',views.marketplace_view,name='marketplace'),
   # path('get-products/', views_original.get_products, name='get_products'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if static path for the images is not mentioned, it will not display images