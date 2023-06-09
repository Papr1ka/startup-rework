from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from colorfield.fields import ColorField

User = get_user_model()

# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=300)
    color = ColorField(default="#FF0000", format="hexa")
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()

class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="model")
    fio = models.CharField(max_length=200, default="Ivanov I.I.")
    about = models.CharField(max_length=1000, blank=True)
    skills = models.ManyToManyField(Skill, related_name="users")
    contacts = models.CharField(max_length=300, blank=True)
    
    def __str__(self) -> str:
        return self.user.username
    
    def __repr__(self) -> str:
        return self.__str__()

class Notification(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=500)
    
    class Meta:
        ordering = ['-id']

class Project(models.Model):
    host = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=100)
    little_description = models.CharField(max_length=500, blank=True, null=True)
    main_description = models.CharField(max_length=50000, blank=True, null=True)
    likes = models.IntegerField(default=0)
    date_of_public = models.DateTimeField(auto_now_add=True)
    applications = models.ManyToManyField(UserModel, related_name="wishing")
    skills = models.ManyToManyField(Skill, related_name="projects")
    
    class Meta:
        ordering = ['-id']
    
    def __str__(self) -> str:
        return self.title
    
    def __repr__(self) -> str:
        return self.__str__()

    
    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})


'''
Необходимые поля 1.Таблицы юзеров(которую необходимо наследовать):
1.1 Логин;(есть в изначальной)
1.2. Пароль(есть в изначальной)
1.3. email(есть в изначальной)
1.4. ФИО
1.5. Дата рождения
1.6. Страна
1.7. Город
1.8. Гражданство
1.9. Пол
1.10. Телефон
1.11. Образование(ВУЗ, специальность, год окончания)
1.12. Занятость
1.13. Опыт работы(лет)
1.14. Навыки
1.15. Достижения/проф. опыт
1.16. Наличие команды(команда проекта)
1.17. роль в команде
1.18. Является ли автором объектов интеллектуальной собственности (есть ли патент)? Если да, то запрос реквизитов документа.
1.19. Реквизиты документа(по ум. None)
1.20. Есть ли своя компания? Если да, то запрос ИНН.
1.21. ИНН(по ум. None)
1.22. поле фотографии
1.23. Описание пользователя
1.24 массив id-шников лайкнутых юзером проектов
1.25 Заполнена ли анкета?(True или False)
1.26 is_activated(Активирован ли аккаунт(по почте), True или False)
2. Таблица ссылок подтверждения почт юзеров(при регистрации на почту будет высылаться ссылка, при переходе на которую юзер будет подтверждать её и соответственно регистрироваться):
2.1. email
2.2. индивидуальная ссылка
3. Таблица проектов:
3.1 Загаловок/Название
3.2. КРАТКОЕ описание
3.3 Основное описание
3.4 Приложения(возможно, какие-то фотографии)
3.5 Владелец проекта
3.6 Необходимые навыки разработчиков для реализации
3.7 количество лайков проекта другими пользователями
3.8 индив. ссылка на проект
3.9 дата публикации
3.10 id привязанной к нему команды разработчиков
3.11 Список заявок на участие(может быть массив из id-шников кандидатов)
4. Таблица команд:
4.1 Массив из id-шников членов команд
4.2 id чата проекта
5. Таблица чатов:
5.1 Сообщение(Массив из словарей вида: {username: 123, message: 123, date: [25.10.22, 0:45])}
'''