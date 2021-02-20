from django.contrib import admin
from .models import Lesson, Subscription, LessonReview, LessonReviewFlagged


class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription

    readonly_fields = ('id',)


class LessonAdmin(admin.ModelAdmin):
    readonly_fields = ('lesson_id',
                       'rating',
                       'is_free')

    fields = ('lesson_id',
              'instructor_profile',
              'lesson_name',
              'card_description',
              'description',
              'image',
              'video_url',
              'rating',
              'time',
              'is_free',
              'price', )

    list_display = (
        'lesson_name',
        'get_instructor_profile',
    )


class LessonReviewAdmin(admin.ModelAdmin):

    fields = ('profile', 'lesson', 'review', 'rating', 'date',)


class LessonReviewFlaggedAdmin(admin.ModelAdmin):
    readonly_fields = ('profile', 'review')

    fields = ('profile', 'review',)


admin.site.register(Lesson, LessonAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(LessonReview, LessonReviewAdmin)
admin.site.register(LessonReviewFlagged,
                    LessonReviewFlaggedAdmin)
