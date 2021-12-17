from django.db import models
from django.contrib.auth.models import User

article = 'ar'
news = 'n'

POST_TYPES = [
    (article, "статья"),
    (news, "новость")
]


# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.FloatField(default=0.0)

    def update_rating(self):
        author_article_rank = 0
        author_comment_rank = 0
        author_article_comment_rank = 0

        author_article_set = Post.objects.filter(author=self, type=article).values("_rank")
        for rank in author_article_set:
            author_article_rank += rank["_rank"] * 3

        author_comment_set = Comment.objects.filter(user=self.user).values("_rank")
        for rank in author_comment_set:
            author_comment_rank += rank["_rank"]

        author_article_id_set = Post.objects.filter(author=self, type=article).values("id")
        for value in author_article_id_set:
            article_comment_set = Comment.objects.filter(post=value["id"]).values("_rank")
            for rank in article_comment_set:
                author_article_comment_rank += rank["_rank"]

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
    _rank = models.IntegerField(default=0, db_column='rank')
    created_datetime = models.DateTimeField(auto_now_add=True)

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        self._rank = int(value) if value >= 0 else 0
        self.save()

    def like(self):
        self.rank += 1
        self.save()

    def dislike(self):
        self.rank -= 1
        self.save()

    def preview(self):
        text = str(self.text)
        if len(text) >= 124:
            return "%s..." % text
        preview = text.split()[:125]
        return "%s..." % preview


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    _rank = models.IntegerField(default=0, db_column='rank')
    created_datetime = models.DateTimeField(auto_now_add=True)

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        self._rank = int(value) if value >= 0 else 0
        self.save()

    def like(self):
        self.rank += 1
        self.save()

    def dislike(self):
        self.rank -= 1
        self.save()
