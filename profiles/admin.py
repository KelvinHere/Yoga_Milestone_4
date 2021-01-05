from django.contrib import admin
from .models import StudentProfile, InstructorProfile


class StudentProfileAdmin(admin.TabularInline):
    model = StudentProfile

    fields = ('user', 'first_name', 'lesson_name',
              'last_name',)


class InstructorProfileAdmin(admin.TabularInline):
    model = InstructorProfile

    fields = ('user', 'first_name', 'last_name',)


admin.site.register(StudentProfile, InstructorProfile)
