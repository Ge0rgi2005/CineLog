from django.urls import path
from .views import (
    MovieListAPIView,
    MovieDetailAPIView,
    ReviewListAPIView,
    GenreListAPIView,
    APIRootView,
)

app_name = 'api'

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('movies/', MovieListAPIView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailAPIView.as_view(), name='movie-detail'),
    path('movies/<int:movie_pk>/reviews/', ReviewListAPIView.as_view(), name='review-list'),
    path('genres/', GenreListAPIView.as_view(), name='genre-list'),
]