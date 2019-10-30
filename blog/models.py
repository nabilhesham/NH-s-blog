from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Post(models.Model):
    objects = models.Manager()   # the default model manager
    published = PublishedManager()   # the customed model manager

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )

    title       =       models.CharField(max_length = 100 )
    slug       =        models.SlugField(max_length= 120 )
    author      =       models.ForeignKey(User, related_name = 'blog_posts', on_delete = models.CASCADE)
    body        =       models.TextField()
    created     =       models.DateTimeField(auto_now_add = True)
    updated     =       models.DateTimeField(auto_now = True)
    status      =       models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft')
    likes       =       models.ManyToManyField(User, related_name='likes', blank=True)

    class Meta :
        ordering = ['-id']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.id, self.slug])

@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return "Profile of User {}".format(self.user.username)

class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.post.title + " image"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.post.title, str(self.user.username))
