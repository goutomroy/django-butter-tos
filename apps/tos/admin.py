from django.contrib import admin
from apps.tos.models import UserTermsOfService, TermsOfService


class UserTermsOfServiceAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'date_accepted']
    search_fields = ['id', 'user']
    readonly_fields = ['id', 'date_accepted', 'profile_at_moment']
    list_display_links = ['id', 'user']


class UserTermsOfServiceInline(admin.TabularInline):
    model = UserTermsOfService
    extra = 1


class TermsOfServiceAdmin(admin.ModelAdmin):

    list_display = ['id', 'slug', 'name', 'version_number', 'status', 'activation_date']
    search_fields = ['id', 'slug']
    readonly_fields = ['id', 'created', 'updated']
    list_display_links = ['id', 'slug']
    ordering = ['-activation_date']
    inlines = [UserTermsOfServiceInline]


admin.site.register(TermsOfService, TermsOfServiceAdmin)
admin.site.register(UserTermsOfService, UserTermsOfServiceAdmin)
