from django.contrib import admin
from django.template.defaultfilters import truncatechars

from app_news.models import *


class CommentInline(admin.TabularInline):
    model = Comment

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'updated_at', 'is_active']
    list_filter = ['is_active']
    list_editable = ['is_active']
    search_fields = ['title']
    actions = ['mark_as_active', 'mark_as_inactive']
    inlines = [CommentInline]

    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)

    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)

    mark_as_active.short_description = 'Change status to active'
    mark_as_inactive.short_description = 'Change status to inactive'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'get_comment_text', 'news']
    list_filter = ['username']
    actions = ['mark_as_deleted']
    list_display_links = ['get_comment_text']

    def get_comment_text(self, obj):
        return truncatechars(obj.comment_text, 15)

    get_comment_text.short_description = 'new comment text'

    def mark_as_deleted(self, request, queryset):
        queryset.update(comment_text='deleted by admin')

    mark_as_deleted.short_description = 'Mark comment as deleted by admin'
