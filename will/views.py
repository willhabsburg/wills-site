"""
Views code for will
"""
# /views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from .forms import RegisterForm

def home(request):
    """ This returns a simple hello world """
    return HttpResponse('Home!')

class HomeView(TemplateView):
    """The Blog homepage"""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)

        return context


class PrivacyView(TemplateView):
    """The Blog homepage"""
    template_name = 'privacy.html'

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)

        return context

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})
