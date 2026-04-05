from rest_framework import serializers
from films.models import Movie, Genre
from reviews.models import Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']


class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = [
            'id',
            'movie_title',
            'director',
            'year',
            'plot',
            'language',
            'duration',
            'genre',
            'average_rating',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'author',
            'title',
            'body',
            'rating',
            'created_at',
        ]
        read_only_fields = ['author', 'created_at']