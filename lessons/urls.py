from django.urls import path
from . import views

urlpatterns = [
    path('', views.lessons, name='lessons'),
    path('my_lessons/', views.my_lessons, name='my_lessons'),
]