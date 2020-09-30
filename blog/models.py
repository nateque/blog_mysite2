from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):

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