from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from films.models import Movie, Genre
from reviews.models import Review

UserModel = get_user_model()


class ReviewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username='reviewer',
            password='Pass1234!',
        )
        self.other_user = UserModel.objects.create_user(
            username='other',
            password='Pass1234!',
        )
        Genre.objects.create(name='Thriller')
        self.movie = Movie.objects.create(
            movie_title='Thriller Film',
            director='Dir',
            year=2019,
            language='en',
        )
        self.review = Review.objects.create(
            author=self.user,
            film=self.movie,
            title='Great Film',
            body='This is a great film with great acting.',
            rating=8,
        )

    def test_review_str(self):
        self.assertEqual(
            str(self.review),
            "reviewer's review of Thriller Film (8/10)"
        )

    def test_review_create_requires_login(self):
        response = self.client.get(
            reverse('reviews:review-create', kwargs={'movie_pk': self.movie.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_only_author_can_edit_review(self):
        self.client.login(username='other', password='Pass1234!')
        response = self.client.get(
            reverse('reviews:review-update', kwargs={'pk': self.review.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_author_can_edit_own_review(self):
        self.client.login(username='reviewer', password='Pass1234!')
        response = self.client.get(
            reverse('reviews:review-update', kwargs={'pk': self.review.pk})
        )
        self.assertEqual(response.status_code, 200)