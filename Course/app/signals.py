from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserModel
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

@receiver(post_save, sender=User)
def createModel(sender, instance, created, **kwargs):
    if created:
        UserModel.objects.create(user=instance, id=instance.id)
    else:
        try:
            instance.model.save()
        except ObjectDoesNotExist:
            UserModel.objects.create(user=instance, id=instance.id)
