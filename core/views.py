from django.views.generic import TemplateView
from films.models import Movie, Genre
from django.shortcuts import render


class LandingPageView(TemplateView):
    template_name = 'core/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_movies'] = Movie.objects.order_by('-created_at')[:6]
        context['genres'] = Genre.objects.all()
        return context

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)