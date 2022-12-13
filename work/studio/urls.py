from django.urls import path
from . import views

urlpatterns = [
    path('', views.studio, name='studio'),
    path('<id>/', views.studio, name='studio'),
]
