from django.contrib import admin

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Article, ArticleRating, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_image', 'order', 'article_count', 'created_at']
    list_editable = ['order']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Articles Count'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'status', 'is_featured', 
                   'view_count', 'display_rating', 'created_at']
    list_filter = ['status', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'content', 'summary']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    autocomplete_fields = ['author', 'category']
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Article Information', {
            'fields': ('title', 'slug', 'summary', 'content')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Relationships', {
            'fields': ('author', 'category')
        }),
        ('Settings', {
            'fields': ('status', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def display_rating(self, obj):
        avg_rating = obj.average_rating
        if avg_rating == 0:
            return "No ratings"
            
        avg_rating = float(avg_rating)
        stars = '★' * int(round(avg_rating))
        empty_stars = '☆' * (5 - int(round(avg_rating)))
        
        return format_html(
            '<span style="color: #FFD700;">{}</span><span style="color: #C0C0C0;">{}</span> ({:.1f})',
            stars, empty_stars, avg_rating
        )
    display_rating.short_description = 'Rating'

    def save_model(self, request, obj, form, change):
        if not change:  # if creating new article
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(ArticleRating)
class ArticleRatingAdmin(admin.ModelAdmin):
    list_display = ['article', 'user', 'score', 'created_at']
    list_filter = ['score', 'created_at']
    search_fields = ['article__title', 'user__email']
    readonly_fields = ['created_at']
    list_per_page = 50

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'short_text', 'is_approved', 
                   'is_reply', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['text', 'user__email', 'article__title']
    list_editable = ['is_approved']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 50

    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Comment'

    def is_reply(self, obj):
        return obj.parent is not None
    is_reply.boolean = True
    is_reply.short_description = 'Is Reply'

    actions = ['approve_comments', 'disapprove_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"

    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "Disapprove selected comments"