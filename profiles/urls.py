from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('instructors/', views.instructors, name='instructors'),
    path('instructor_profile/<instructor_id>', views.instructor_profile, name='instructor_profile'),
]
