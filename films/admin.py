from django.contrib import admin
from .models import Genre, Movie, CastMember


class CastMemberInline(admin.TabularInline):
    model = CastMember
    extra = 1


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Movie)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('movie_title', 'director', 'year', 'language', 'average_rating')
    list_filter = ('language', 'genre', 'year')
    search_fields = ('movie_title', 'director')
    filter_horizontal = ('genre',)
    inlines = [CastMemberInline]


@admin.register(CastMember)
class CastMemberAdmin(admin.ModelAdmin):
    list_display = ('person_name', 'person_role', 'character_name', 'movie')
    list_filter = ('person_role',)
    search_fields = ('person_name', 'movie__movie_title')