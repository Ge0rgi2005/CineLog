from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import MovieForm, CastMemberForm
from .models import Movie, Genre


class MovieListView(ListView):
    model = Movie
    template_name = 'films/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        queryset = Movie.objects.prefetch_related('genre')
        genre_slug = self.request.GET.get('genre')
        search = self.request.GET.get('search')

        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)
        if search:
            queryset = queryset.filter(movie_title__icontains=search)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['selected_genre'] = self.request.GET.get('genre', '')
        context['search'] = self.request.GET.get('search', '')
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'films/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cast'] = self.object.cast.all()
        context['reviews'] = self.object.reviews.order_by('-created_at')
        context['user_review'] = None
        if self.request.user.is_authenticated:
            context['user_review'] = self.object.reviews.filter(
                author=self.request.user
            ).first()
        return context


class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'films/movie_form.html'

    def get_success_url(self):
        return reverse_lazy('films:movie-detail', kwargs={'pk': self.object.pk})


class MovieUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = 'films/movie_form.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(
            name='Critics'
        ).exists()

    def get_success_url(self):
        return reverse_lazy('films:movie-detail', kwargs={'pk': self.object.pk})


class MovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movie
    template_name = 'films/movie_confirm_delete.html'
    success_url = reverse_lazy('films:movie-list')

    def test_func(self):
        return self.request.user.is_staff


class CastMemberCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = CastMemberForm
    template_name = 'films/cast_member_form.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(
            name='Critics'
        ).exists()

    def form_valid(self, form):
        form.instance.movie = Movie.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('films:movie-detail', kwargs={'pk': self.kwargs['pk']})