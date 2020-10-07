from django.shortcuts import render, redirect, get_object_or_404, Http404
from .models import Post, Image_post, Comment
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, PostForm, PostEditForm, ImageForm, CommentForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import modelformset_factory
from django.contrib import messages

# Create your views here.
def home(request):

    post_list = Post.published.all()
    query = request.GET.get('q')

    if query:
        post_list = Post.published.filter(
        Q(title__icontains=query) |
        Q(author__username=query) |
        Q(body__icontains=query)
    )

    paginator = Paginator(post_list, 2) # Show 2 posts per page
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
    }
    template_name = 'blog/home.html'
    return render(request, template_name, context)

def detailPost(request, pk, slug):

    post = get_object_or_404(Post, id=pk, slug=slug)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    
    if not request.user.is_authenticated:
        return Http404('Please login to comment on posts.')
    else:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST or None)
            if comment_form.is_valid():
                content = comment_form.cleaned_data.get('content')
                reply_id = request.POST.get('reply_id')
                reply_comment = None
                if reply_id:
                    reply_comment = Comment.objects.get(id=reply_id)
                comment = Comment.objects.create(post=post, content=content, user=request.user, reply=reply_comment)
                comment.save()
                return redirect(post.get_absolute_url())

        else:
            comment_form = CommentForm()

    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'comments': comments,
        'comment_form': comment_form,
    }
    template_name = 'blog/detail.html'
    return render(request, template_name, context)


def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return redirect(post.get_absolute_url())


@login_required(login_url= 'login')
def createPost(request):
    # ImageFormset = modelformset_factory(Image_post, form=ImageForm, extra=3, max_num=3)

    if request.method == 'POST':
        form = PostForm(request.POST or None)
        # formset = ImageFormset(request.POST or None, request.FILES or None, queryset=Image_post.objects.none())
        if form.is_valid(): #and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # for form in formset:
            #     photo = form.cleaned_data.get('image')
            #     image = Image_post(post=post, image=photo)
            #     image.save()
            messages.success(request, f"Post has been created successfully.")
            return redirect('home')

    else:
        form = PostForm()
        # formset = ImageFormset(queryset=Image_post.objects.none())

    context = {
        'form': form,
        # 'formset': formset,
    }
    template_name = 'blog/create.html'
    return render(request, template_name, context)


def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404()
    else:
        if request.method == 'POST':
            form = PostEditForm(request.POST or None, instance=post)
            if form.is_valid():
                form.save()
                post_title = form.cleaned_data.get('title')
                messages.info(request, f"Post '{post_title}' has been edited successfully.")
                return redirect(post.get_absolute_url())
        else:
            form = PostEditForm(instance=post)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/edit.html', context)


def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404()
    else:
        post.delete()
        messages.error(request, f"Post '{post}' has been deleted successfully.")
        return redirect('home')

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
                messages.success(request, f"User '{username}' logged in successfully.")
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
    messages.success(request, f"Logged out successfully.")
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
                messages.success(request, f"User '{username}' has been registered and logged in successfully.")
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
            username = user_form.cleaned_data.get('username')
            messages.success(request, f"User '{username}' profile has been updated successfully.")
            return redirect('home')
    else:
        user_form       = UserEditForm(instance=request.user)
        profile_form    = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/edit_profile.html', context)

def delete_comment(request, id):

    comment = Comment.objects.get(id=id)
    
    if comment.post.author == request.user or comment.user == request.user:
        comment.delete()
        messages.error(request, f"Comment has been deleted successfully.")
        return redirect(comment.post.get_absolute_url())
    else:
        Http404()