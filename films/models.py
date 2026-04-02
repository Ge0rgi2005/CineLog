from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Movie(models.Model):
    LANGUAGE_OPTIONS = [
        ('en', 'English'),
        ('fr', 'French'),
        ('de', 'German'),
        ('es', 'Spanish'),
        ('it', 'Italian'),
        ('jp', 'Japanese'),
        ('kr', 'Korean'),
        ('?', 'Other Languages'),
    ]

    movie_title = models.CharField(
        max_length=200,
    )
    director = models.CharField(
        max_length=200,
    )
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1888),
            MaxValueValidator(9999),
        ],
    )
    plot = models.TextField(
        blank=True,
        null=True,
    )
    poster = models.ImageField(
        upload_to='posters/',
        blank=True,
        null=True,
    )
    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_OPTIONS,
        default='en',
    )
    duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='How long the movie is (in minutes)',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='movies',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', 'movie_title']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        constraints = [
            models.UniqueConstraint(
                fields=['movie_title', 'year', 'director'],
                name='unique_movie'
            )
        ]

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.duration is not None and self.duration < 1:
            raise ValidationError({'duration': 'The movie must be at least a minute long.'})

    def __str__(self):
        return f"{self.movie_title} ({self.year})"

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return None
        return round(sum(r.rating for r in reviews) / len(reviews), 1)


class CastMember(models.Model):
    ROLE_OPTIONS = [
        ('a_m', 'Actor'),
        ('a_f', 'Actress'),
        ('d', 'Director'),
        ('p', 'Producer'),
        ('c', 'Composer'),
        ('w', 'Writer'),
    ]

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='cast',
    )
    person_name = models.CharField(max_length=255)
    person_role = models.CharField(
        max_length=20,
        choices=ROLE_OPTIONS,
        default='a_m',
    )
    character_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Character name if applicable.",
    )

    class Meta:
        ordering = ['person_name']
        verbose_name = 'Cast Member'
        verbose_name_plural = 'Cast Members'

    def __str__(self):
        return f"{self.person_name} as {self.character_name or self.person_role} in {self.movie.movie_title}"