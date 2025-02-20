from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from .resources import POST_TYPES


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    """
    According to the terms of reference, the overall rating of the author is determined by the amount:
    - triple total rating of all posts by the author
    - the total rating of all the author's comments
    - the total rating of all comments on the author's articles
    """

    def update_rating(self):
        sum_rating_post_author_3 = Post.objects.filter(author=self).aggregate(Sum('rating_post')) * 3
        sum_rating_comment_author = Comment.objects.filter(user=self.user).aggregate(Sum('rating_comment'))
        sum_rating_comment_post_author = Comment.objects.filter(post__author=self).aggregate(Sum('rating_comment'))

        self.rating_author = sum_rating_post_author_3 + sum_rating_comment_author + sum_rating_comment_post_author
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(choices=POST_TYPES, max_length=2, default='NW')
    date_time_in = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=50)
    content = models.TextField()
    rating_post = models.IntegerField(default=0)

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        if len(self.content) > 124:
            return self.content[:124] + '...'
        else:
            return self.content


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_time_in = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()