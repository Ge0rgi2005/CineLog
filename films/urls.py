from django.urls import path
from .views import (
    MovieListView,
    MovieDetailView,
    MovieCreateView,
    MovieUpdateView,
    MovieDeleteView,
    CastMemberCreateView,
)

app_name = 'films'

urlpatterns = [
    path('', MovieListView.as_view(), name='movie-list'),
    path('<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('create/', MovieCreateView.as_view(), name='movie-create'),
    path('<int:pk>/edit/', MovieUpdateView.as_view(), name='movie-update'),
    path('<int:pk>/delete/', MovieDeleteView.as_view(), name='movie-delete'),
    path('<int:pk>/cast/add/', CastMemberCreateView.as_view(), name='cast-add'),
]