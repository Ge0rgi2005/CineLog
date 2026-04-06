from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from films.models import Movie, Genre

UserModel = get_user_model()


class MovieModelTests(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Drama')
        self.movie = Movie.objects.create(
            movie_title='Test Film',
            director='Test Director',
            year=2020,
            language='en',
        )
        self.movie.genre.add(self.genre)

    def test_movie_str(self):
        self.assertEqual(str(self.movie), 'Test Film (2020)')

    def test_genre_slug_auto_generated(self):
        self.assertEqual(self.genre.slug, 'drama')

    def test_movie_average_rating_no_reviews(self):
        self.assertIsNone(self.movie.average_rating)


class MovieViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.genre = Genre.objects.create(name='Action')
        self.movie = Movie.objects.create(
            movie_title='Action Movie',
            director='Director',
            year=2021,
            language='en',
        )
        self.staff_user = UserModel.objects.create_user(
            username='staff',
            password='Pass1234!',
            is_staff=True,
        )
        self.regular_user = UserModel.objects.create_user(
            username='regular',
            password='Pass1234!',
        )

    def test_movie_list_loads(self):
        response = self.client.get(reverse('films:movie-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Action Movie')

    def test_movie_detail_loads(self):
        response = self.client.get(
            reverse('films:movie-detail', kwargs={'pk': self.movie.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Action Movie')

    def test_movie_create_requires_login(self):
        response = self.client.get(reverse('films:movie-create'))
        self.assertEqual(response.status_code, 302)

    def test_movie_create_accessible_to_staff(self):
        self.client.login(username='staff', password='Pass1234!')
        response = self.client.get(reverse('films:movie-create'))
        self.assertEqual(response.status_code, 200)

    def test_movie_search_filters_results(self):
        Movie.objects.create(
            movie_title='Another Film',
            director='Someone',
            year=2022,
            language='en',
        )
        response = self.client.get(
            reverse('films:movie-list') + '?search=Action'
        )
        self.assertContains(response, 'Action Movie')
        self.assertNotContains(response, 'Another Film')