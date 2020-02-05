from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save


def upload_location(instance, filename, **kwargs):
    file_path = f'blog/{str(instance.author.id)}/{str(instance.title)}-{filename}'
    return file_path


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_COICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, unique=True)
    image = models.ImageField(
        upload_to=upload_location, null=False, blank=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField(null=False, blank=False)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_COICES, default='draft')
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month, self.publish.day, self.slug])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish']


# @receiver(post_delete, sender=Post)
# def submission_delete(sender, instance, **kwargs):
#     instance.image.delete(False)


# def pre_save_blog_post_receiever(sender, instance, **kwargs):
#     if not instance.slug:
#         instance.slug = slugify(instance.author.username+'-'+instance.title)


# pre_save.connect(pre_save_blog_post_receiever, sender=Post)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

# # class like(models.Model()):
