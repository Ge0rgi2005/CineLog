from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings


class Review(models.Model):
    review_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    reviewed_movie = models.ForeignKey(
        'films.Movie',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    review_title = models.CharField(
        max_length=255,
        help_text="The title of the user's full review.",
    )
    full_review = models.TextField(
        help_text="The user's full review",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        help_text="The user's rating on a 1-10 scale.",
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Featured reviews appear on the movie's main page.",
    )
    written_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-written_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['review_author', 'reviewed_movie'],
                name='unique_review_per_user_per_movie'
            )
        ]

    def clean(self):
        if self.full_review and len(self.full_review.strip()) < 10:
            raise ValidationError({'full_review': 'The review must be at least 10 characters long.'})

    def __str__(self):
        return f"{self.review_author.username}'s review of {self.reviewed_movie.movie_title} ({self.rating}/10)"


class ReviewComment(models.Model):
    commented_review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    comment_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='review_comments',
    )
    comment_body = models.TextField()
    written_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['written_at']
        verbose_name = 'Review Comment'
        verbose_name_plural = 'Review Comments'

    def clean(self):
        if self.comment_body and len(self.comment_body.strip()) < 2:
            raise ValidationError({'review_body': 'Comment must be at least 2 characters.'})

    def __str__(self):
        return f"Comment by {self.comment_author.username} on {self.commented_review}"