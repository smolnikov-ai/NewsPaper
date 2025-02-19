from tkinter.constants import CASCADE

from django.db import models


class Author(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    rating_author = models.FloatField(default=0.0)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    date_time_in = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=50)
    content = models.TextField()
    rating_post = models.FloatField(default=0.0)


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField()
    date_time_in = models.DateTimeField(auto_now_add=True)
    rating_comment = models.FloatField(default=0.0)