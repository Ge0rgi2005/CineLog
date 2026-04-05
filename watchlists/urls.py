from django.urls import path
from .views import (
    WatchlistListView,
    WatchlistDetailView,
    WatchlistCreateView,
    WatchlistUpdateView,
    WatchlistDeleteView,
    AddToWatchlistView,
    RemoveFromWatchlistView,
)

app_name = 'watchlists'

urlpatterns = [
    path('', WatchlistListView.as_view(), name='watchlist-list'),
    path('<int:pk>/', WatchlistDetailView.as_view(), name='watchlist-detail'),
    path('create/', WatchlistCreateView.as_view(), name='watchlist-create'),
    path('<int:pk>/edit/', WatchlistUpdateView.as_view(), name='watchlist-update'),
    path('<int:pk>/delete/', WatchlistDeleteView.as_view(), name='watchlist-delete'),
    path('<int:pk>/add/', AddToWatchlistView.as_view(), name='add-to-watchlist'),
    path('entry/<int:pk>/remove/', RemoveFromWatchlistView.as_view(), name='remove-from-watchlist'),
]