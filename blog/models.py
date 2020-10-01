from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")

class Post(models.Model):

    objects = models.Manager() #Our default manager
    published = PublishedManager() #Our Custom model manager

    CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title       =   models.CharField(max_length=120, unique=True)
    slug        =   models.SlugField(max_length=140, unique=True)
    author      =   models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body        =   models.TextField()
    created     =   models.DateTimeField(auto_now_add=True)
    updated     =   models.DateTimeField(auto_now=True)
    status      =   models.CharField(max_length=20, choices=CHOICES, default='draft')

    def __str__(self):
        return f'{self.title}'

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