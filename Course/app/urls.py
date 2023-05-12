from django.urls import path, include
from .views import (
    HomeView,
    RegisterView,
    LoginView,
    LogoutView,
    PasswordResetView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    ProjectRespondView,
    SkillCreateView,
    SkillDeleteView,
    CabinetView,
    SummaryUpdateView,
    RespondsDetailView,
    RespondAgreeView,
    RespondDisagreeView,
    NotificationsView,
)

urlpatterns = [
    #Серсис авторизации
    path('register', RegisterView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('reset_password/', PasswordResetView.as_view(), name="password_reset"),
    
    #Сервис идей
    path('', HomeView.as_view(), name="home"),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name="project_detail"),
    path('project/create/', ProjectCreateView.as_view(), name="project_create"),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name="project_update"),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name="project_delete"),
    path('project/<int:pk>/respond/', ProjectRespondView.as_view(), name="project_respond"),
    path('skill/create/', SkillCreateView.as_view(), name="skill_create"),
    path('skill/<int:pk>/delete/', SkillDeleteView.as_view(), name="skill_delete"),
    
    #Личный кабинет
    path('cabinet/', CabinetView.as_view(), name="cabinet"),
    path('cabinet/summary/', SummaryUpdateView.as_view(), name="summary"),
    path('cabinet/responds/', RespondsDetailView.as_view(), name="responds"),
    path('cabinet/responds/<int:project_id>/<int:pk>/agree/', RespondAgreeView.as_view(), name="respond_agree"),
    path('cabinet/responds/<int:project_id>/<int:pk>/disagree/', RespondDisagreeView.as_view(), name="respond_disagree"),
    path('cabinet/notifications/', NotificationsView.as_view(), name="notifications"),
]
