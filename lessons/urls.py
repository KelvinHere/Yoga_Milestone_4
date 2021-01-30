from django.urls import path
from . import views

urlpatterns = [
    path('', views.lessons, name='lessons'),
    path('instructor_created_lessons/', views.instructor_created_lessons, name='instructor_created_lessons'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('create_lesson/', views.create_lesson, name='create_lesson'),
    path('edit_lesson/<lesson_id>', views.edit_lesson, name='edit_lesson'),
    path('delete_instructor_created_lesson/<id>', views.delete_instructor_created_lesson, name='delete_instructor_created_lesson'),
    path('review_lesson/<lesson_id>', views.review_lesson, name='review_lesson'),
    path('delete_review/<lesson_id>', views.delete_review, name='delete_review'),
    path('flag_review/<review_pk>/<lesson_id>', views.flag_review, name='flag_review'),
    path('get_modal_data/', views.get_modal_data, name='get_modal_data'),
]
