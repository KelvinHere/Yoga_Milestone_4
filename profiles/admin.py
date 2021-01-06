from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.TabularInline):
    model = UserProfile

    fields = ('user', 'first_name', 'last_name',
              'is_instructor',)


admin.site.register(UserProfile)

