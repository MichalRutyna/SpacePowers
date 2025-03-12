from django.contrib import admin

from .models import *


class CommentInlineAdmin(admin.TabularInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = False
    save_on_top = True
    list_display = ('id', 'title', 'nation', 'author', 'category',  'created_at', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('category', 'category', 'tags', 'nation', 'author', 'created_at', 'is_published')
    readonly_fields = ('views', 'created_at', 'seen_by')
    fields = ('title', 'slug', 'author', 'nation',  'category', 'tags', 'content', 'roll', 'seen_by', 'views', 'created_at')
    inlines = (CommentInlineAdmin,)

    list_editable = ('is_published',)

    def comments(self, obj):
        return ", ".join([str(a) for a in obj.comments.all()])

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'comment', 'author', 'created_at', 'is_published')
    list_display_links = ('id', 'author', 'post')
    list_filter = ('post', 'created_at', 'is_published', 'is_published')
    search_fields = ('author', 'post__title')
    actions = ['publish_comments', 'unpublish_comments']

    list_editable = ('is_published',)

    def publish_comments(self, request, queryset):
        queryset.update(is_published=True)

    publish_comments.short_description = "Publish selected comments"

    def unpublish_comments(self, request, queryset):
        queryset.update(is_published=False)

    unpublish_comments.short_description = "Unpublish selected comments"



admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)