from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):

    objects = models.Manager() # Default Model Manager
    published = PublishedManager() # Our Custom Model Manager

    CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title           =   models.CharField(max_length=120, unique=True)
    slug            =   models.SlugField(max_length=140, unique=True)
    author          =   models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body            =   models.TextField()
    likes           =   models.ManyToManyField(User, blank=True, related_name='likes')
    created         =   models.DateTimeField(auto_now_add=True)
    updated         =   models.DateTimeField(auto_now=True)
    status          =   models.CharField(max_length=20, choices=CHOICES, default='draft')
    restrict_comment=   models.BooleanField(default=False)

    class Meta:
        ordering = ['-created'] # latest Order_by posts

    def __str__(self):
        return f'{self.title}'

    def total_likes(self):
        return f'{self.likes.count()}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk, 'slug': self.slug})


@receiver(pre_save, sender= Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug


class Profile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    dob     = models.DateField(blank=True, null=True)
    photo   = models.ImageField(default='photos/profile.jpg', upload_to='photos/%Y/%m/%d/')

    def __str__(self):
        return f"Profile of {self.user.username} User"


class Image_post(models.Model):
    post    = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    image   = models.ImageField(upload_to='post_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.post} images'

class Comment(models.Model):
    post        = models.ForeignKey(Post, on_delete=models.CASCADE)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    content     = models.TextField(max_length=160)
    reply       = models.ForeignKey('self', null=True,  on_delete=models.CASCADE, related_name='replies')
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} - {self.user.username}"
