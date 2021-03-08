from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy, reverse
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserLoginForm


class UserSignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse_lazy('login')


class UserSignInView(LoginView):
    model = CustomUser
    form_class = CustomUserLoginForm
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        return super(LoginView, self).get(request, *args, **kwargs)


class CoWorkersListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/coworkers.html'

    def get_queryset(self):
        queryset = CustomUser.objects.exclude(id=self.request.user.id)
        return queryset
