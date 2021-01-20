from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_basket, name='view_basket'),
    path('add_to_basket/<lesson_id>/', views.add_to_basket, name='add_to_basket'),
]
