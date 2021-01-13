from django.contrib import admin
from .models import UserProfile
from lessons.models import LessonItem


class LessonItemAdmin(admin.TabularInline):
    model = LessonItem

    fields = ('lesson', 'user')


class UserProfileAdmin(admin.ModelAdmin):
    #readonly_fields = ('requested_instructor_status',)
    inlines = (LessonItemAdmin,)


    model = UserProfile

    fields = ('user', 'first_name', 'last_name',
              'requested_instructor_status',
              'is_instructor', 'card_description',
              'profile_description', 'image',
              'rating',)


admin.site.register(UserProfile, UserProfileAdmin)

