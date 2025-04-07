from django.contrib import admin
from django.utils.html import format_html, mark_safe, format_html_join

from .models import *

class RollInLine(admin.TabularInline):
    model = Roll
    extra = 0
    fields = ['roll', 'roll_description', 'roll_type']
    classes = ['collapse']

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = False
    save_on_top = True
    list_display = ('id', 'title', 'nation', 'author', 'category',  'created_at', 'is_published', 'approved_by_admin')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    readonly_fields = ('views', 'created_at', 'edited_at', 'seen_by', 'comments', 'is_published')
    list_filter = ('category', 'tags', 'nation', 'author', 'created_at',)
    inlines = [RollInLine,]
    list_editable = ('approved_by_admin',)
    view_on_site = True

    fieldsets = [
        (
            None,
            {
                "fields": ["title", ("author", "nation"), ("tags", "arcs"), "content"]
            }
        ),
        (
            "Interactions",
            {
                "fields": ["comments", "liked_by", 'update_subscribe']
            }
        ),
        (
            "Misc info",
            {
                "fields": ['seen_by', 'views', 'created_at', 'edited_at', 'edited']
            }
        ),
        (
            "Advanced settings",
            {
                "fields": ["slug", "category", ("is_published", "published_by_user", "approved_by_admin", "published_override"), ("success_roll_override", "secrecy_roll_override"), "active",],
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
admin.site.register(Arc)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
