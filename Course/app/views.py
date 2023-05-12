from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.views.generic import CreateView, FormView, RedirectView, DetailView
from django.urls import reverse_lazy
from .models import *
from . import signals

# Create your views here.
class HomeView(View):
    def get(self, request):
        cards = [
                {
            "seens": 1000,
            "maxTeam": 5,
            "team": 3,
            "title": "Lorem Ipsum - это текст-\"рыба\", часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной \"рыбой\" Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsu...",
            "text": "В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum для распечатки образцов. Lorem Ipsum не только успешно пережил без заметных изменений пять веков, но и перешагнул в электронный дизайн. Его популяризации в новое время послужили публикация листов Letraset с образцами Lorem Ipsum в 60-х годах и, в более недавнее время, программы электронной вёрстки типа Aldus...",
            "professions": [{"text": "frontend", "color": "#FAFF00"}, {"text": "backend", "color": "#FF0000"}, {"text": "devops", "color": "#00FF29"}, {"text": "engineer", "color": "#FF00FF"}]
        } for i in range(10)
        ]
        
        categories = [
            "Devops",
            "JQuery",
            "Новые",
            "24ч",
            "ML",
            "Data Science",
        ]
        
        return render(request, "app/home.html", context={'cards': cards, 'categories': categories})

class LoginView(FormView):
    form_class = AuthenticationForm
    model = get_user_model()
    template_name = "app/auth.html"
    success_url = reverse_lazy("home")

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        
        return super().form_valid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    model = get_user_model()
    template_name = "app/auth.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        r = super().form_valid(form)
        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)
        return r

class LogoutView(RedirectView):
    permanent = True
    url = reverse_lazy("home")

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

class ProjectDetailView(DetailView):
    model = Project
    template_name = "app/project.html"

class ProjectCreateView(FormView):
    form_class = ProjectForm
    model = Project
    template_name = "app/form.html"
    url = None
    
    def get_success_url(self) -> str:
        return self.url

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.host = self.request.user.model
        obj.save()
        self.url = obj.get_absolute_url()
        return super().form_valid(form)

class PasswordResetView(FormView):
    form_class = PasswordResetForm
    model = User
    template_name = "app/form.html"
    success_url = reverse_lazy("home")

    def form_invalid(self, form: Any) -> HttpResponse:

        return super().form_invalid(form)