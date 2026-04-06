from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_welcome_email(username, email):
    send_mail(
        subject='Welcome to CineLog!',
        message=f'Hi {username},\n\nWelcome to CineLog! '
                f'Start logging your favourite films today.\n\nThe CineLog Team',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )


@shared_task
def send_review_notification(review_id):
    from reviews.models import Review
    try:
        review = Review.objects.select_related('author', 'movie').get(pk=review_id)
        send_mail(
            subject=f'New activity on your review of {review.reviewed_movie.movie_title}',
            message=f'Hi {review.review_author.username},\n\n'
                    f'Someone commented on your review of '
                    f'"{review.reviewed_movie.movie_title}". '
                    f'Log in to CineLog to check it out!\n\nThe CineLog Team',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[review.review_author.email],
            fail_silently=True,
        )
    except Review.DoesNotExist:
        pass