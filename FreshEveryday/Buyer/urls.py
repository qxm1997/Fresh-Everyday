from django.urls import path
from Buyer.views import *
urlpatterns = [
    path('register/', register),
    path('login/', login),

]