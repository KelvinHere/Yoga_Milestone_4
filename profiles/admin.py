from django.contrib import admin
from .models import UserProfile
from lessons.models import LessonItem


class LessonItemAdmin(admin.TabularInline):
    model = LessonItem

    fields = ('lesson', 'user')


class UserProfileAdmin(admin.ModelAdmin):
    inlines = (LessonItemAdmin,)
    

    model = UserProfile

    fields = ('user', 'first_name', 'last_name',
              'is_instructor', 'card_description',
              'profile_description', 'image',
              'rating',)


admin.site.register(UserProfile, UserProfileAdmin)

