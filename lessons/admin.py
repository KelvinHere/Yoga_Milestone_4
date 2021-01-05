from django.contrib import admin
from .models import Lesson


class LessonAdmin(admin.TabularInline):
    model = Lesson

    readonly_fields = ('lesson_id')

    fields = ('lesson_id', 'instructor_name', 'lesson_name',
              'description', 'lesson_url',)


admin.site.register(Lesson)
