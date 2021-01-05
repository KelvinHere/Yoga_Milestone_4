from django.contrib import admin
from .models import Lesson, LessonItem


class LessonItemAdmin(admin.ModelAdmin):
    model = LessonItem


class LessonAdmin(admin.ModelAdmin):
    inlines = (LessonItemAdmin)

    readonly_fields = ('lesson_id')

    fields = ('lesson_id', 'instructor_name', 'lesson_name',
              'description', 'lesson_url',)

    list_display = (
        'lesson_name',
        'get_instructor_name',
    )


admin.site.register(Lesson)
admin.site.register(LessonItem)