from django.db import models
from django.contrib.auth.models import User
class Site(models.Model):
    name =  models.CharField(max_length=50,default='')
    score = models.IntegerField(default=0)
    user_score = models.IntegerField(default=0)

class Author(models.Model):
    score = models.IntegerField(default=0)

class Article(models.Model):
    site = models.ForeignKey(Site)
    author = models.ForeignKey(Author)
    score = models.IntegerField(default=0)
    grammar_error_count = models.IntegerField(default=0)
    spell_error_count = models.IntegerField(default=0)
    style_error_count = models.IntegerField(default=0)
    word_count = models.IntegerField(default=0)
    content = models.TextField()


class Review(models.Model):
    article = models.ForeignKey(Article)
    user = models.ForeignKey(User)
    comment = models.TextField()
    upvote_count = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
