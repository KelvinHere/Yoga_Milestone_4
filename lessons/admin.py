from django.contrib import admin
from .models import Lesson, LessonItem


class LessonItemAdmin(admin.ModelAdmin):
    model = LessonItem

    readonly_fields = ('id',)


class LessonAdmin(admin.ModelAdmin):
    readonly_fields = ('lesson_id',)

    fields = ('lesson_id', 'instructor_profile', 'lesson_name',
              'card_description', 'description', 'url', 'image',
              'image_url', 'rating', 'yoga_style',)

    list_display = (
        'lesson_name',
        'get_instructor_profile',
    )


admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonItem, LessonItemAdmin)