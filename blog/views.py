from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):

    posts = Post.published.all().order_by('created')

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

@login_required(login_url= 'login')
def createPost(request):

    if request.method == 'POST':
        title   =   request.POST['title']
        body    =   request.POST['content']
        status  =   request.POST['status']

        form = Post(title=title, body=body, status=status, author=request.user)
        form.save()
        return redirect('home')
    else:
        form = Post()

    context = {}
    template_name = 'blog/create.html'
    return render(request, template_name, context)


def user_login(request):

    if request.method == 'POST':
        # form = UserLoginForm(request.POST or None)
        # if form.is_valid():
        username    =   request.POST['username']
        password    =   request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('home')
    # else:
    #     form = UserLoginForm()

    context = {
        # 'form': form,
    }
    template_name = 'accounts/login.html'
    return render(request, template_name, context)

def user_logout(request):

    auth.logout(request)
    return redirect('login')


def user_registration(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            # we are logging him directly
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }
    template_name = 'accounts/register.html'
    return render(request, template_name, context)

@login_required(login_url= 'login')
def profileEdit(request):
    if request.method == 'POST':
        user_form       = UserEditForm(data= request.POST or None, instance=request.user)
        profile_form    = ProfileEditForm(data= request.POST or None, instance=request.user.profile, files= request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('home')
    else:
        user_form       = UserEditForm(instance=request.user)
        profile_form    = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/edit_profile.html', context)
