from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView


class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('main')
        else:
            return reverse_lazy('main')


class RegisterView(FormView):
    template_name = 'user/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        if user.is_staff:
            return redirect('main')
        else:
            return redirect('main')


class LogoutView(LogoutView):
    next_page = reverse_lazy('login')