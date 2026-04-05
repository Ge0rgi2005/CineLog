from django.views.generic import TemplateView
from films.models import Movie, Genre


class LandingPageView(TemplateView):
    template_name = 'core/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_movies'] = Movie.objects.order_by('-created_at')[:6]
        context['genres'] = Genre.objects.all()
        return context