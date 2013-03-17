from django.db import models

class Site(models.Model):
    score = models.IntegerField(default=0)
    user_score = models.IntegerField(default=0)

class Author(models.Model):
    score = models.IntegerField(default=0)

class Article(models.Model):
    site = models.ForeignKey(Site)
    author = models.ForeignKey(Author)
    score = models.IntegerField(default=0)
    content = models.TextField()

class User(models.Model):
    name = models.CharField(max_length=10)

class Review(models.Model):
    article = models.ForeignKey(Article)
    user = models.ForeignKey(User)
    comment = models.TextField()
    score = models.IntegerField(default=0)
