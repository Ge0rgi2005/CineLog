from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Watchlist(models.Model):
    list_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='watchlists',
    )
    list_title = models.CharField(
        max_length=255,
        help_text="Give your watchlist a name.",
    )
    list_description = models.TextField(
        blank=True,
        null=True,
    )
    listed_movies = models.ManyToManyField(
        'films.Movie',
        related_name='watchlists',
        blank=True,
        through='WatchlistEntry',
    )
    is_public = models.BooleanField(
        default=True,
        help_text="Public watchlists are visible to all users.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Watchlist'
        verbose_name_plural = 'Watchlists'
        constraints = [
            models.UniqueConstraint(
                fields=['list_owner', 'list_title'],
                name='unique_watchlist_title_per_user'
            )
        ]

    def clean(self):
        if self.list_title and len(self.list_title.strip()) < 3:
            raise ValidationError({'title': 'Watchlist title must be at least 3 characters.'})

    def __str__(self):
        return f"{self.list_title} by {self.list_owner.username}"

    @property
    def movie_count(self):
        return self.listed_movies.count()


class WatchlistEntry(models.Model):
    watchlist = models.ForeignKey(
        Watchlist,
        on_delete=models.CASCADE,
        related_name='entries',
    )
    movie = models.ForeignKey(
        'films.Movie',
        on_delete=models.CASCADE,
        related_name='watchlist_entries',
    )
    added_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Your thoughts on why you want to see the movie.",
    )
    is_watched = models.BooleanField(
        default=False,
        help_text="Once you've seen the movie, mark it as watched.",
    )

    class Meta:
        ordering = ['-added_at']
        verbose_name = 'Watchlist Entry'
        verbose_name_plural = 'Watchlist Entries'
        constraints = [
            models.UniqueConstraint(
                fields=['watchlist', 'movie'],
                name='unique_movie_per_watchlist'
            )
        ]

    def __str__(self):
        return f"{self.movie.movie_title} in {self.watchlist.list_title}"