from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

AVATAR_DEFAULT = 'users/avatar.jpg'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=255, blank=True, null=True, default=None)
    avatar = models.ImageField(upload_to='users/', default=AVATAR_DEFAULT)

    @property
    def is_custom_avatar(self):
        return self.avatar != AVATAR_DEFAULT

    @property
    def avatar_default(self):
        return AVATAR_DEFAULT

    def __str__(self):
        return "{}".format(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
