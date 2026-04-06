from django.contrib import admin
from .models import Review, ReviewComment


class ReviewCommentInline(admin.TabularInline):
    model = ReviewComment
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'film', 'rating', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'rating')
    search_fields = ('author__username', 'film__movie_title')
    inlines = [ReviewCommentInline]


@admin.register(ReviewComment)
class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'review', 'created_at')
    search_fields = ('author__username',)