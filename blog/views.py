from django.shortcuts import render, redirect, get_object_or_404
from .models import Post

# Create your views here.
def home(request):

    posts = Post.objects.all().order_by('created')

    context = {
        'posts': posts,
    }
    template_name = 'blog/home.html'
    return render(request, template_name, context)

def detailPost(request, pk, slug):

    post = get_object_or_404(Post, id=pk, slug=slug)

    context = {
        'post': post,
    }
    template_name = 'blog/detail.html'
    return render(request, template_name, context)