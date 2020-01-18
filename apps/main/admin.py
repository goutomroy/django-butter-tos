from django.contrib import admin
from apps.main.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'street', 'postal_code']
    search_fields = ['id', 'user__email', 'user__username']
    readonly_fields = ['id', 'created', 'updated']
    list_display_links = ['id', 'user']
    ordering = ['-created']


admin.site.register(UserProfile, UserProfileAdmin)
