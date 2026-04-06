from celery import shared_task


@shared_task
def send_watchlist_digest():
    from django.contrib.auth import get_user_model
    from django.core.mail import send_mail
    from django.conf import settings
    from watchlists.models import WatchlistEntry

    UserModel = get_user_model()
    users = UserModel.objects.filter(
        watchlists__isnull=False
    ).distinct()

    sent = 0
    for user in users:
        unwatched = WatchlistEntry.objects.filter(
            watchlist__list_owner=user,
            is_watched=False,
        ).select_related('movie')[:5]

        if not unwatched or not user.email:
            continue

        movie_list = '\n'.join(
            f'- {entry.movie.movie_title} ({entry.movie.year})'
            for entry in unwatched
        )

        send_mail(
            subject='Your CineLog Weekly Watchlist Digest',
            message=f'Hi {user.username},\n\n'
                    f'Here are some movies waiting on your watchlist:\n\n'
                    f'{movie_list}\n\n'
                    f'Happy watching!\nThe CineLog Team',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        sent += 1

    return f'Digest sent to {sent} users.'