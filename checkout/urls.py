from django.contrib import admin
from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
    path('attach_basket_to_intent/', views.attach_basket_to_intent, name='attach_basket_to_intent'),
    path('wh/', webhook, name='webhook')
]