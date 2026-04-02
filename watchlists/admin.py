from django.contrib import admin
from .models import Watchlist, WatchlistEntry


class WatchlistEntryInline(admin.TabularInline):
    model = WatchlistEntry
    extra = 0


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('list_title', 'list_owner', 'is_public', 'movie_count', 'created_at')
    list_filter = ('is_public',)
    search_fields = ('list_title', 'list_owner__username')
    inlines = [WatchlistEntryInline]


@admin.register(WatchlistEntry)
class WatchlistEntryAdmin(admin.ModelAdmin):
    list_display = ('movie', 'watchlist', 'is_watched', 'added_at')
    list_filter = ('is_watched',)
