from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.CalEvent)
class CalAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'name',
        'date',
        'group',
        'isAnniv',
    )
    list_filter = (
        'owner',
        'group',
    )
    search_fields = (
        'owner',
        'name',
        'date'
    )
    
@admin.register(models.EventGroup)
class EventGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'owner',
        'private',
    )
    list_filter = (
        'name',
        'owner',
    )
    search_fields = (
        'name',
        'owner',
    )