from django.contrib import admin
from django.utils.html import format_html, mark_safe, format_html_join

from .models import *

class RollInLine(admin.TabularInline):
    model = Roll
    extra = 0
    fields = ['roll', 'roll_description', 'roll_type']

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = False
    save_on_top = True
    list_display = ('id', 'title', 'nation', 'author', 'category',  'created_at', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('category', 'tags', 'nation', 'author', 'created_at', 'is_published')
    readonly_fields = ('views', 'created_at', 'seen_by', 'comments')
    inlines = [RollInLine,]
    list_editable = ('is_published',)
    view_on_site = True

    fieldsets = [
        (
            None,
            {
                "fields": ["title", ("author", "nation"), "tags", "content"]
            }
        ),
        (
            "Interactions",
            {
                "fields": ["comments", "liked_by"]
            }
        ),
        (
            "Misc info",
            {
                "fields": ['seen_by', 'views', 'created_at']
            }
        ),
        (
            "Advanced settings",
            {
                "fields": ["slug", "category", ("success_roll_override", "secrecy_roll_override")],
                "classes": ("collapse",),
            }
        )
    ]


    def comments(self, obj):
        return format_html_join("",
                                "<a href=\"{}\">{}</a><br>",
                                ((mark_safe(reverse("admin:News_comment_change", args=(a.pk,))), str(a)) for a in obj.comments.all())
                                )

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'success_roll_required', 'secrecy_roll_required')


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
