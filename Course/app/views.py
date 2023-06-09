from typing import Any, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.views.generic import CreateView, FormView, RedirectView, DetailView, DeleteView, ListView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import *
from . import signals
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView

class RequiredSuperUserMixin(UserPassesTestMixin):
    permission_denied_message = "Not found"
    raise_exception = True
    
    def test_func(self):
        return self.request.user.is_superuser

class LoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")

def is_valid_queryparam(param):
    return param != '' and param is not None

def is_int(param):
    try:
        int(param)
    except:
        return False
    else:
        return True

class HomeView(ListView):
    model = Project
    template_name = "app/home.html"
    context_object_name = "cards"
    queryset = Project.objects.all()
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        context['skills'] = Skill.objects.all()
        
        return context

    def get(self, request, *args, **kwargs):
        
        if request.GET.get("query"):
            query = request.GET.get("query")
            self.queryset = Project.objects.filter(Q(title__icontains=query) | Q(little_description__icontains=query) | Q(main_description__icontains=query)).distinct()
            return super().get(request, *args, **kwargs)
        
        query = Q()
        order = 0
        
        for param in request.GET:
            if is_valid_queryparam(param):
                if param.startswith("skills"):
                    skill = request.GET.get(param)
                    if is_int(skill):
                        query = query & (Q(skills=int(skill)))
                elif param.startswith("sorting"):
                    sorting = request.GET.get(param)
                    if is_int(sorting):
                        order = int(sorting)
        
        
        
        self.queryset = Project.objects.filter(query).distinct()
        if order == 1:
            self.queryset = self.queryset.order_by("id")
        
        return super().get(request, *args, **kwargs)

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

class LogoutView(LoginRequiredMixin, RedirectView):
    permanent = True
    url = reverse_lazy("home")

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

class ProjectDetailView(DetailView):
    model = Project
    template_name = "app/project.html"

class ProjectCreateView(LoginRequiredMixin, FormView):
    form_class = ProjectForm
    model = Project
    template_name = "app/project_create.html"
    url = None
    
    def get_success_url(self) -> str:
        return self.url

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.host = self.request.user.model
        skills = form.cleaned_data.get("skills")
        obj.save()
        if skills:
            for skill in skills:
                obj.skills.add(skill)
        self.url = obj.get_absolute_url()
        return super().form_valid(form)

class ProjectUpdateView(UpdateView, ProjectCreateView):
    
    def post(self, request, *args, **kwargs):
        try:
            user = UserModel.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect(reverse("app:login"))
        obj = self.get_object()
        
        if obj.host == user:
            return super().post(request, *args, **kwargs)
        else:
            raise PermissionDenied

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "app/object_delete.html"
    success_url = reverse_lazy("home")
    
    def post(self, request, *args, **kwargs):
        try:
            user = UserModel.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect(reverse("login"))
        obj = self.get_object()
        
        if obj.host == user:
            return super().post(request, *args, **kwargs)
        else:
            raise PermissionDenied
    

class PasswordResetView(PasswordResetView):
    template_name = "app/form.html"

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "app/form.html"

class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "app/message.html"
    
    def get_context_data(self, **kwargs: Any) -> Any:
        r = super().get_context_data(**kwargs)
        r['message'] = "Письмо отправлено, проверяйте почту"
        return r

class ProjectRespondView(LoginRequiredMixin, DetailView):
    permanent = True
    url = reverse_lazy("home")
    template_name = "app/message.html"
    model = Project
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        r = super().get_context_data(**kwargs)
        r['message'] = "Отклик успешно отправлен"
        return r
    
    def get(self, request, *args, **kwargs):
        r = super().get(request, *args, **kwargs)
        try:
            user = UserModel.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect(reverse("login"))
        if self.object.applications.contains(user):
           return render(request, self.template_name, context={"message": "Вы уже подали заявку"})
        self.object.applications.add(user)
        return r


class SkillCreateView(LoginRequiredMixin, CreateView):
    form_class = SkillForm
    model = Skill
    template_name = "app/form.html"
    success_url = reverse_lazy("home")
    
class SkillDeleteView(RequiredSuperUserMixin, DeleteView):
    model = Skill
    template_name = "app/form.html"
    success_url = reverse_lazy("home")

class CabinetView(LoginRequiredMixin, UpdateView):
    template_name = "app/cabinet.html"
    form_class = UserInfoForm
    model = User
    success_url = reverse_lazy("cabinet")
    
    def get_object(self, *args, **kwargs):
        model = self.request.user
        return model

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        model = self.get_object()
        kwargs.update({'pk': model.pk})
        return super().get(request, *args, **kwargs)

class SummaryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "app/summary.html"
    form_class = UserModelInfoForm
    model = UserModel
    success_url = reverse_lazy("summary")

    def get_object(self, *args, **kwargs):
        model = UserModel.objects.get(user=self.request.user)
        return model

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        model = self.get_object()
        kwargs.update({'pk': model.pk})
        return super().get(request, *args, **kwargs)

class RespondsDetailView(LoginRequiredMixin, ListView):
    template_name = "app/responds.html"

    def get_queryset(self) -> QuerySet[Any]:
        user = UserModel.objects.get(user=self.request.user)
        qs = Project.objects.filter(host=user)
        return qs

class RespondAgreeView(LoginRequiredMixin, View):
    def post(self, request, project_id=None, pk=None):
        user = request.user
        model = UserModel.objects.get(user=user)
        try:
            obj = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            return HttpRequest("Объект не найден")
        if obj.host != model:
            raise PermissionDenied
        try:
            respondent = UserModel.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return HttpRequest("Пользователь не найден")
        if respondent.wishing.contains(obj):
            obj.applications.remove(respondent)
            Notification.objects.create(user=respondent, message=f"Вас ВЗЯЛИ в проект {obj.title}, контакты: {obj.host.contacts}")
            return redirect(reverse("responds"))
        else:
            return HttpResponse("Что вы имели ввиду?")

class RespondDisagreeView(LoginRequiredMixin, View):
    def post(self, request, project_id=None, pk=None):
        user = request.user
        model = UserModel.objects.get(user=user)
        try:
            obj = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            return HttpRequest("Объект не найден")
        if obj.host != model:
            raise PermissionDenied
        try:
            respondent = UserModel.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return HttpRequest("Пользователь не найден")
        if respondent.wishing.contains(obj):
            obj.applications.remove(respondent)
            Notification.objects.create(user=respondent, message=f"Вас НЕ ВЗЯЛИ в проект {obj.title}")
        else:
            return HttpResponse("Что вы имели ввиду?")

class NotificationsView(LoginRequiredMixin, ListView):
    template_name = "app/notifications.html"

    def get_queryset(self) -> QuerySet[Any]:
        user = UserModel.objects.get(user=self.request.user)
        qs = user.notifications.all()
        return qs

class DeleteAccountView(LoginRequiredMixin, TemplateView):
    template_name = "app/message.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(message="Ваша аккаунт успешно удалён")
        return context

    def get(self, request, *args, **kwargs):
        UserModel.objects.filter(user=request.user).delete()
        User.objects.filter(id=request.user.id).delete()
        logout(self.request)
        return super().get(request, *args, **kwargs)
