from django.forms import ModelForm, ValidationError
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import Project, Skill, UserModel

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean(self):
        email = self.cleaned_data['email']
        if not email or User.objects.filter(email=email).exists():
            raise ValidationError("User with this email alredy exists")
        return super().clean()
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "little_description", "main_description", "skills"]

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name"]

class UserModelInfoForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["fio", "skills", "about", "contacts"]

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]
    
    def clean(self):
        username = self.cleaned_data['username']
        if not username or User.objects.filter(username=username).exists():
            raise ValidationError("User with this username alredy exists")
        return super().clean()
