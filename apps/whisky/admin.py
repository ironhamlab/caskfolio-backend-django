from django.contrib import admin
from .models import Whisky, CaskType


@admin.register(CaskType)
class CaskTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Whisky)
class WhiskyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'distillery', 'country', 'whisky_type', 'region', 'peat_level', 'price_tier')
    list_filter = ('country', 'whisky_type', 'region', 'peat_level', 'price_tier')
    search_fields = ('name', 'distillery')
    filter_horizontal = ('cask_types',)
