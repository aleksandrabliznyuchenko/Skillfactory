from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache

tank, heal, dd, merch, guildmaster, questgiver, blasksmith, tanner, potionmaker, spellmaker = \
    "t", "h", "dd", "m", "gm", "qg", "bs", "tn", "pm", "sm"

POST_CATEGORIES = [
    (tank, "Танки"),
    (heal, "Хилы"),
    (dd, "ДД"),
    (merch, "Торговцы"),
    (guildmaster, "Гилдмастеры"),
    (questgiver, "Квестгиверы"),
    (blasksmith, "Кузнецы"),
    (tanner, "Кожевенники"),
    (potionmaker, "Зельевары"),
    (spellmaker, "Мастера заклинаний"),
]


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.CharField(max_length=2,
                                choices=POST_CATEGORIES,
                                default=tank)
    header = models.CharField(max_length=255)
    text = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.header} {self.text}'

    def get_absolute_url(self):
        return f'/posts/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    def preview(self):
        text = str(self.text)
        if len(text) <= 124:
            return text
        preview = text[:125]
        return "%s..." % preview


class Reply(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
