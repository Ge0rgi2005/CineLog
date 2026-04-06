from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings


class Review(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    film = models.ForeignKey(
        'films.Movie',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.CharField(
        max_length=255,
        help_text="Give your review a title.",
    )
    body = models.TextField(
        help_text="Write your full review here.",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        help_text="Rate the film from 1 to 10.",
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Featured reviews appear on the film's main page.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        # One review per user per film
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'film'],
                name='unique_review_per_user_per_film'
            )
        ]

    def clean(self):
        if self.body and len(self.body.strip()) < 10:
            raise ValidationError({'body': 'Review body must be at least 10 characters long.'})

    def __str__(self):
        return f"{self.author.username}'s review of {self.film.title} ({self.rating}/10)"


class ReviewComment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='review_comments',
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Review Comment'
        verbose_name_plural = 'Review Comments'

    def clean(self):
        if self.body and len(self.body.strip()) < 2:
            raise ValidationError({'body': 'Comment must be at least 2 characters.'})

    def __str__(self):
        return f"Comment by {self.author.username} on {self.review}"