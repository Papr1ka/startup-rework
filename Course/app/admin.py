from django.contrib import admin
from .models import UserModel, Project, Skill

# Register your models here.
admin.site.register(UserModel)
admin.site.register(Project)
admin.site.register(Skill)
