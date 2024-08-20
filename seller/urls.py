from django.urls import path
from seller.views import *
from app.views import *

urlpatterns = [
    path('seller/',register_seller),
    path('sel/',seller),
    path('log/',enterview),
    path('sellerpage/',seller_index),
    path('product/',product),
    path('productdis/',productdisplay),
    path('seldel/<int:id>',seldelete),
    path('selup/<int:id>',selupdate),
    
]

