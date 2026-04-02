from django.contrib import admin
from .models import Review, ReviewComment


class ReviewCommentInline(admin.TabularInline):
    model = ReviewComment
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_author', 'reviewed_movie', 'rating', 'is_featured', 'written_at')
    list_filter = ('is_featured', 'rating')
    search_fields = ('review_author__username', 'review_title')
    inlines = [ReviewCommentInline]


@admin.register(ReviewComment)
class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('comment_author', 'commented_review', 'written_at')
    search_fields = ('comment_author__username',)