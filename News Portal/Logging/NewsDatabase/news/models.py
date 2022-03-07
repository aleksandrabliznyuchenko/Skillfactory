from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache

article = 'ar'
news = 'n'

POST_TYPES = [
    (article, "статья"),
    (news, "новость")
]


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)

    def update_rating(self):
        author_article_rank = 0
        author_comment_rank = 0
        author_article_comment_rank = 0

        author_article_set = Post.objects.filter(author=self, type=article).values("rank")
        for rank in author_article_set:
            author_article_rank += rank["rank"] * 3

        author_comment_set = Comment.objects.filter(user=self.user).values("rank")
        for rank in author_comment_set:
            author_comment_rank += rank["rank"]

        author_article_id_set = Post.objects.filter(author=self, type=article).values("id")
        for value in author_article_id_set:
            article_comment_set = Comment.objects.filter(post=value["id"]).values("rank")
            for rank in article_comment_set:
                author_article_comment_rank += rank["rank"]

        self.rank = author_article_rank + author_comment_rank + author_article_comment_rank
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255,
                            unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')
    type = models.CharField(max_length=2,
                            choices=POST_TYPES,
                            default=article)
    header = models.CharField(max_length=255)
    text = models.TextField()
    rank = models.IntegerField(default=0)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.header} {self.text}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    def like(self):
        self.rank += 1
        self.save()

    def dislike(self):
        self.rank -= 1
        self.save()

    def preview(self):
        text = str(self.text)
        if len(text) <= 124:
            return text
        preview = text[:125]
        return "%s..." % preview


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rank = models.IntegerField(default=0)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.rank += 1
        self.save()

    def dislike(self):
        self.rank -= 1
        self.save()


# class UserCategory(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     category = models.ManyToManyField(Category)
#     created_datetime = models.DateTimeField(auto_now_add=True)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    created_datetime = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
