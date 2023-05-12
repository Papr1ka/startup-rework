from django.urls import path, include
from .views import HomeView, RegisterView, LoginView, LogoutView, ProjectDetailView, ProjectCreateView, PasswordResetView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('register', RegisterView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name="project_detail"),
    path('project/create/', ProjectCreateView.as_view(), name="project_create"),
    path('reset_password/', PasswordResetView.as_view(), name="password_reset"),
]
