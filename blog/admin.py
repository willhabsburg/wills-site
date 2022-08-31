from django.contrib import admin
from . import models
from blog.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created',
    )
    list_filter = (
        'name',
        'approved',
    )
    search_fields = (
        'text',
        'name__username',
        'name__first_name',
        'name__last_name',
    )

class CommentInline(admin.TabularInline):
    model = Comment
    fk_name = "post"
    """
    Thanks to https://stackoverflow.com/questions/17118320/how-to-add-readonly-inline-on-django-admin for the readonly fields
    """
    fields = ('name', 'email', 'text', 'approved')
    readonly_fields = ('name', 'email', 'text')
    """
    Thanks to https://cmsdk.com/python/how-hide-delete-item-in-django-admin-tabularinline.html for no delete button
    """
    def has_delete_permission(self, request, obj=None):
        return False

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created',
        'updated',
    )
    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )
    list_filter = (
        'status',
        'topics',
    )
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CommentInline,]

class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    list_filter = (
        'name',
    )
    prepopulated_fields = {'slug': ('name',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created',
    )
    list_filter = (
        'name',
        'approved',
    )
    search_fields = (
        'text',
        'name',
    )

admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Comment, CommentAdmin)

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'last_name',
        'first_name',
        'submitted'
    )
    # Make these fields read-only in the admin
    readonly_fields = (
        'first_name',
        'last_name',
        'email',
        'message',
        'submitted'
    )

@admin.register(models.PhotoContest)
class PhotoContestAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'photo'
    )
    list_filter = (
        'name',
        'email',
    )
    search_fields = (
        'name',
        'email',
    )
    # Make these fields read-only in the admin
    readonly_fields = (
        'name',
        'email',
        'photo',
        'submitted'
    )
