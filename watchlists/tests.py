from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from films.models import Movie, Genre
from watchlists.models import Watchlist, WatchlistEntry

UserModel = get_user_model()


class WatchlistTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username='watcher',
            password='Pass1234!',
        )
        self.other_user = UserModel.objects.create_user(
            username='other',
            password='Pass1234!',
        )
        self.watchlist = Watchlist.objects.create(
            list_owner=self.user,
            list_title='My Favourites',
            is_public=True,
        )
        genre = Genre.objects.create(name='Comedy')
        self.movie = Movie.objects.create(
            movie_title='Comedy Film',
            director='Dir',
            year=2018,
            language='en',
        )

    def test_watchlist_str(self):
        self.assertEqual(str(self.watchlist), 'My Favourites by watcher')

    def test_public_watchlist_visible_to_anonymous(self):
        response = self.client.get(reverse('watchlists:watchlist-list'))
        self.assertContains(response, 'My Favourites')

    def test_watchlist_create_requires_login(self):
        response = self.client.get(reverse('watchlists:watchlist-create'))
        self.assertEqual(response.status_code, 302)

    def test_only_owner_can_edit_watchlist(self):
        self.client.login(username='other', password='Pass1234!')
        response = self.client.get(
            reverse('watchlists:watchlist-update', kwargs={'pk': self.watchlist.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_movie_count_property(self):
        WatchlistEntry.objects.create(
            watchlist=self.watchlist,
            movie=self.movie,
        )
        self.assertEqual(self.watchlist.movie_count, 1)