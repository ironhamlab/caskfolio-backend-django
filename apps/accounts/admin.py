from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'nickname', 'is_active', 'created_at', 'deleted_at')
    list_filter = ('is_active', 'theme')
    search_fields = ('email', 'nickname')
    ordering = ('-created_at',)

    fieldsets = UserAdmin.fieldsets + (
        ('추가 정보', {
            'fields': ('nickname', 'bio', 'theme', 'note_default_public', 'deleted_at')
        }),
    )