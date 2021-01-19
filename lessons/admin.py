from django.contrib import admin
from .models import Lesson, LessonItem, LessonReview


class LessonItemAdmin(admin.ModelAdmin):
    model = LessonItem

    readonly_fields = ('id',)


class LessonAdmin(admin.ModelAdmin):
    readonly_fields = ('lesson_id',)

    fields = ('lesson_id', 'instructor_profile', 'lesson_name',
              'card_description', 'description', 'image',
              'video_url', 'rating', 'yoga_style', 'time', )

    list_display = (
        'lesson_name',
        'get_instructor_profile',
    )


class LessonReviewAdmin(admin.ModelAdmin):

    fields = ('profile', 'lesson', 'review', 'rating', 'date',)


admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonItem, LessonItemAdmin)
admin.site.register(LessonReview, LessonReviewAdmin)
