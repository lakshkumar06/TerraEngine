from django.contrib import admin
from .models import MarsSite


@admin.register(MarsSite)
class MarsSiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'lat', 'lon']
    list_filter = ['location']
    search_fields = ['name', 'location']
    readonly_fields = ['created_at', 'updated_at']
