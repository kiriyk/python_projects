from django.contrib import admin

from app_media.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
