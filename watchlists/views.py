from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from films.models import Movie
from .forms import WatchlistForm, WatchlistEntryForm
from .models import Watchlist, WatchlistEntry


class WatchlistListView(ListView):
    model = Watchlist
    template_name = 'watchlists/watchlist_list.html'
    context_object_name = 'watchlists'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Watchlist.objects.filter(
                list_owner=self.request.user
            ).order_by('-created_at')
        return Watchlist.objects.filter(is_public=True).order_by('-created_at')


class WatchlistDetailView(DetailView):
    model = Watchlist
    template_name = 'watchlists/watchlist_detail.html'
    context_object_name = 'watchlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entries'] = self.object.entries.select_related('movie').all()
        context['entry_form'] = WatchlistEntryForm(
            initial={'watchlist': self.object}
        )
        return context


class WatchlistCreateView(LoginRequiredMixin, CreateView):
    model = Watchlist
    form_class = WatchlistForm
    template_name = 'watchlists/watchlist_form.html'

    def form_valid(self, form):
        form.instance.list_owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('watchlists:watchlist-detail', kwargs={'pk': self.object.pk})


class WatchlistUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Watchlist
    form_class = WatchlistForm
    template_name = 'watchlists/watchlist_form.html'

    def test_func(self):
        return self.get_object().list_owner == self.request.user

    def get_success_url(self):
        return reverse_lazy('watchlists:watchlist-detail', kwargs={'pk': self.object.pk})


class WatchlistDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Watchlist
    template_name = 'watchlists/watchlist_confirm_delete.html'
    success_url = reverse_lazy('watchlists:watchlist-list')

    def test_func(self):
        return self.get_object().list_owner == self.request.user


class AddToWatchlistView(LoginRequiredMixin, View):
    def post(self, request, pk):
        watchlist = get_object_or_404(Watchlist, pk=pk, list_owner=request.user)
        movie_pk = request.POST.get('movie')
        movie = get_object_or_404(Movie, pk=movie_pk)


        WatchlistEntry.objects.get_or_create(
            watchlist=watchlist,
            movie=movie,
        )
        return redirect('watchlists:watchlist-detail', pk=watchlist.pk)


class RemoveFromWatchlistView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WatchlistEntry
    template_name = 'watchlists/entry_confirm_delete.html'

    def test_func(self):
        return self.get_object().watchlist.list_owner == self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'watchlists:watchlist-detail',
            kwargs={'pk': self.object.watchlist.pk}
        )