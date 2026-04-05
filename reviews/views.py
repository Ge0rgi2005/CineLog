from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import ReviewForm, ReviewCommentForm
from .models import Review


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['movie'] = self.kwargs.get('movie_pk')
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('films:movie-detail', kwargs={'pk': self.object.movie.pk})


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy('films:movie-detail', kwargs={'pk': self.object.movie.pk})


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy('films:movie-detail', kwargs={'pk': self.object.movie.pk})


class ReviewCommentCreateView(LoginRequiredMixin, CreateView):
    form_class = ReviewCommentForm
    template_name = 'reviews/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.review_id = self.kwargs['review_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'films:movie-detail',
            kwargs={'pk': self.object.review.movie.pk}
        )
