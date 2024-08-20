from django.urls import path
from app.views import *
urlpatterns = [

    path('',index),
    path('register/',register),
    path('login/',view_login),
    path('user/',userprofile),
    path('viewdet/<int:id>',viewdet),
    path('update/',updatepro),
    path('product/',product),
    path('add/<int:id>',addtocart),
    path('cartdis/',cartdisplay),
    path('inc/<int:itemid>',inc_increment),
    path('wish/<int:id>',addtowish),
    path('wishdis/',wishdisplay),
    path('delete/<int:id>',delete),
    path('delwish/<int:id>',deletewish),
    path('adress/',Adress),
    path('adrview/',deliverydet),
    path('summary/',summarypage),
    path('charge/',charges),
    path('create/',createorder),
    path('orders/',orderview),
    path('ord/<int:id>',ordercancel),
    path('orderconfirm/',createorder),
    path('changepass/',change_user_password),
    path('logout/',logout),
   
]