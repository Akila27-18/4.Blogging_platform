
from django.contrib import admin
from .models import Post, Comment, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title","author","created_at")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("author","categories")
    search_fields = ("title","content")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post","user","approved","created_at")
    list_filter = ("approved",)
    search_fields = ("text",)
    actions = ["approve_selected"]

    @admin.action(description="Approve selected comments")
    def approve_selected(self, request, queryset):
        queryset.update(approved=True)

admin.site.register(Category)
