from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Post, Tag, User, Like
from .forms import PostForm, CreateUserForm, AddComment

def create_page_obj(request, post_list):
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    tag = request.GET.get("tag", 0)
    post_list = (
        Post.objects.filter(is_hidden=False).order_by('-pub_date')
    )
    page_obj = create_page_obj(request, post_list)
    tag_list = Tag.objects.all()
    context = {
        'page_obj': page_obj,
        'tag_list': tag_list,
    }
    return render(
        request,
        'pages/index.html',
        context,
    )


def user_page(request, user_id):
    user = get_object_or_404(User, id=user_id)
    post_list = (
        Post.objects.filter(author__username=user).order_by('-pub_date')
    )
    page_obj = create_page_obj(request, post_list)
    context = {
        'user': user,
        'page_obj': page_obj,
    }
    return render(request, 'pages/user_page.html', context)


def post_page(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = request.user
    like = False
    if Like.objects.filter(user=author.id, post=post.id).exists():
        like = True
    context = {
        'post': post,
        'like': like,
    }
    return render(request, 'pages/post_page.html', context)


def create(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            username = request.user
            instance.author = username
            instance.save()
            return redirect('pages:index')
        return render(
            request,
            'pages/create.html',
            {'form': form, 'is_edit': False}
        )
    return render(
        request,
        'pages/create.html',
        {'form': form, 'is_edit': False}
    )


def moderation(request):
    form = AddComment(request.POST or None)
    post_list = (
        Post.objects.filter(is_hidden=True).order_by('-pub_date')
    )
    page_obj = create_page_obj(request, post_list)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            post = form.cleaned_data.get('post')
            post.is_hidden = True
            post.save()
            instance.save()
            return redirect('pages:moderation')
        return render(
            request,
            'pages/moderation.html',
            {'form': form, 'is_edit': False, 'page_obj': page_obj,}
        )
    return render(
        request,
        'pages/moderation.html',
        {'form': form, 'page_obj': page_obj,}
    )


def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = request.user
    if not Like.objects.filter(user=author.id, post=post.id).exists():
        Like.objects.create(user=author, post=post, value=1.0)
    else:
        Like.objects.filter(user=author.id, post=post.id).delete()
    return redirect('pages:post_page', post_id=post_id)


class SignUp(CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy('pages:index')
    template_name = 'users/signup.html'
