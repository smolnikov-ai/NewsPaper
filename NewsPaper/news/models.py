from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .resources import POST_TYPES


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    """
    According to the terms of reference, the overall rating of the author is determined by the amount:
    - triple total rating of all posts by the author
    - the total rating of all the author's comments
    - the total rating of all comments on the author's articles

    It starts when a reaction (like/dislike, post/comment) is added
    """

    def update_rating(self):
        sum_rating_post_author_3 = Post.objects.filter(author=self). \
            aggregate(rp=Coalesce(Sum('rating_post'), 0))['rp'] * 3
        sum_rating_comment_author = Comment.objects.filter(user=self.user). \
            aggregate(rca=Coalesce(Sum('rating_comment'), 0))['rca']
        sum_rating_comment_post_author = Comment.objects.filter(post__author=self). \
            aggregate(rcpa=Coalesce(Sum('rating_comment'), 0))['rcpa']
        ## or
        # sum_rating_post_author_3 = self.post__set.aggregate(rp=Coalesce(Sum('rating_post'), 0)).get('rp') * 3
        # sum_rating_comment_author = self.user.comment__set.aggregate(rca=Coalesce(Sum('rating_comment'), 0)).get('rca')
        # sum_rating_comment_post_author = self.post__set.aggregate(rcpa=Coalesce(Sum('comment__rating_comment'), 0)).get('rcpa')

        self.rating_author = sum_rating_post_author_3 + sum_rating_comment_author + sum_rating_comment_post_author
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True, help_text=_('category name'), verbose_name=_('category'),)
    subscribers = models.ManyToManyField(User, through='UserCategory', related_name='categories')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, help_text=_('author name'), verbose_name=_('author'),)
    type = models.CharField(choices=POST_TYPES, max_length=2, default='NW',
                            help_text=_('post type'), verbose_name=_('type'),)
    date_time_in = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory', help_text=_('categories of post'),
                                        verbose_name=_('categories'),)
    title = models.CharField(max_length=50, help_text=_('post title'), verbose_name=_('title'),)
    content = models.TextField(help_text=_('post content'), verbose_name=_('content'),)
    rating_post = models.IntegerField(default=0, help_text=_('post rating'), verbose_name=_('rating'),)

    def like(self):
        self.rating_post += 1
        self.save()
        # after adding the reaction, update the rating of the author
        self.author.update_rating()

    def dislike(self):
        self.rating_post -= 1
        self.save()
        # after adding the reaction, update the rating of the author
        self.author.update_rating()

    def preview(self):
        if len(self.content) > 124:
            return self.content[:124] + '...'
        else:
            return self.content

    def __str__(self):
        return f'{self.title.title()}: {self.content[:124]}'

    def get_absolute_url(self):
        #return reverse('post_detail', args=[str(self.pk)])
        #return reverse('post_detail', args=[str(self.id)])
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_time_in = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()
        # after adding the reaction, update the rating of the authors
        Author.objects.get(user=self.user).update_rating()
        self.post.author.update_rating()

    def dislike(self):
        self.rating_comment -= 1
        self.save()
        # after adding the reaction, update the rating of the authors
        Author.objects.get(user=self.user).update_rating()
        self.post.author.update_rating()


# Модель связи User и Category для поля subscribers модели Category
class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)