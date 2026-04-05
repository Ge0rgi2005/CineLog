from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from films.models import Movie, Genre
from reviews.models import Review
from .serializers import MovieSerializer, GenreSerializer, ReviewSerializer


class MovieListAPIView(generics.ListAPIView):
    queryset = Movie.objects.prefetch_related('genre').all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


class MovieDetailAPIView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


class ReviewListAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(
            movie_id=self.kwargs['movie_pk']
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            movie_id=self.kwargs['movie_pk']
        )


class GenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]


class APIRootView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            'movies': '/api/movies/',
            'genres': '/api/genres/',
            'reviews': '/api/movies/{id}/reviews/',
        })