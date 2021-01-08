from django.urls import path
from . import views

urlpatterns = [
    path('', views.lessons, name='lessons'),
    path('my_lessons/', views.my_lessons, name='my_lessons'),
    path('instructor_created_lessons/', views.instructor_created_lessons, name='instructor_created_lessons'),
    path('unsubscribe_lesson/<lesson>/<origin>', views.unsubscribe_lesson, name='unsubscribe_lesson'),
    path('subscribe_lesson/<int:id>', views.subscribe_lesson, name='subscribe_lesson'),
    path('create_lesson/', views.create_lesson, name='create_lesson'),
    path('edit_lesson/<lesson_id>', views.edit_lesson, name='edit_lesson'),
    path('delete_instructor_created_lesson/<id>', views.delete_instructor_created_lesson, name='delete_instructor_created_lesson'),
    
]

