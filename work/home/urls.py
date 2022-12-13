from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('info/', views.info, name='info'),
    path('superuser_admin/', views.superuser_admin, name='superuser_admin'),
    path('update_instructor_status/<user_to_update>/<status>',
         views.update_instructor_status,
         name='update_instructor_status'),
]
