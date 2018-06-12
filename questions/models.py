from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

AVATAR_DEFAULT = 'users/avatar.jpg'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=255, blank=True, null=True, default=None)
    avatar = models.ImageField(upload_to='users/', default=AVATAR_DEFAULT)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

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


class Tag(models.Model):
    tagword = models.CharField(max_length=64)

    def __str__(self):
        return "{}".format(self.tagword)


class Question(models.Model):
    """заголовок,	содержание,	автор,	дата	создания,	тэги"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField(Tag,  verbose_name="list of tags",
                                  blank=True, default=None)
    likes = models.ManyToManyField(User,  verbose_name="q_liked from",
                                   default=None, related_name="q_liked_from")
    dislikes = models.ManyToManyField(User, verbose_name="q_disliked from",
                                      default=None, related_name="q_disliked_from")
    rating = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "{}".format(self.title[:50])


class Answer(models.Model):
    """содержание,	автор,	дата	написания,	флаг	правильного	ответа"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    is_solution = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, verbose_name="a_liked from",
                                   default=None, related_name="a_liked_from")
    dislikes = models.ManyToManyField(User, verbose_name="a_disliked from",
                                      default=None, related_name="a_disliked_from")
    rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "{}".format(self.content[:50])


class Invite(models.Model):
    """регистрация по инвайтам"""
    token = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    user_id_from = models.IntegerField(default=0)  # чей токен
    user_id_to = models.IntegerField(default=0)  # кто им воспользовался
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
