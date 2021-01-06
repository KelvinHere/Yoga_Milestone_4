from django.urls import path
from . import views

urlpatterns = [
    path('', views.lessons, name='lessons'),
    path('my_lessons/', views.my_lessons, name='my_lessons'),
    path('instructor_created_lessons/', views.instructor_created_lessons, name='instructor_created_lessons'),
]

