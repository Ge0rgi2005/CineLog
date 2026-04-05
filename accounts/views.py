from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from .forms import RegisterForm, LoginForm, EditProfileForm

UserModel = get_user_model()


class RegisterView(CreateView):
    model = UserModel
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('films:movie-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('films:movie-list'))
        return super().dispatch(request, *args, **kwargs)

class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('core:landing')


class ProfileView(DetailView):
    model = UserModel
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        context['reviews'] = profile_user.reviews.order_by('-created_at')[:5]
        context['watchlists'] = profile_user.watchlists.filter(
            is_public=True
        ).order_by('-created_at')[:5]
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = EditProfileForm
    template_name = 'accounts/profile_editor.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy ('accounts:profile', kwargs={'pk': self.request.user.pk})