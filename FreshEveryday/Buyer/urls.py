from django.urls import path
from Buyer.views import *
urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('detail/', detail),
    path('goodlist/', goods_list),
    path('address/', address),
    path('sda/', setDefaultAddress),
    path('addcart/', add_cart),
    path('cart/', cart),
    path('palceorder/', palce_order),
    path('save_order/', save_order),
    path('hhh/', hhh),

]

urlpatterns += [



]