from celery import shared_task


@shared_task
def update_movie_ratings():
    from films.models import Movie
    from django.db.models import Avg

    movies = Movie.objects.prefetch_related('reviews')
    updated = 0

    for movie in movies:
        avg = movie.reviews.aggregate(Avg('rating'))['rating__avg']
        if avg is not None:
            updated += 1

    return f'Processed ratings for {updated} movies.'


@shared_task
def cleanup_unreviewed_castmembers():
    from films.models import CastMember
    orphaned = CastMember.objects.filter(movie__isnull=True)
    count = orphaned.count()
    orphaned.delete()
    return f'Cleaned up {count} orphaned cast members.'