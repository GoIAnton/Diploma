from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import datetime

from .models import Publication, Tag, User, Like, Comment
from .forms import PublicationForm, CreateUserForm, CreateComment


def create_page(request, publications):
    pages = Paginator(publications, 10)
    page_number = request.GET.get('page')
    return pages.get_page(page_number)


def index(request):
    tags = request.GET.getlist('tag')
    type = request.GET.getlist('type')
    if tags:
        if 'news' in type:
            publications = (
                Publication.objects.filter(is_hidden=False, tags__slug__in=tags, is_article=False).order_by('-pub_date').distinct()
                )
        elif 'article' in type:
            publications = (
                Publication.objects.filter(is_hidden=False, tags__slug__in=tags, is_article=True).order_by('-pub_date').distinct()
                )
        else:
            publications = (
                Publication.objects.filter(is_hidden=False, tags__slug__in=tags).order_by('-pub_date').distinct()
            )
    else:
        if 'news' in type:
            publications = (
                Publication.objects.filter(is_hidden=False, is_article=False).order_by('-pub_date').distinct()
                )
        elif 'article' in type:
            publications = (
                Publication.objects.filter(is_hidden=False, is_article=True).order_by('-pub_date').distinct()
                )
        else:
            publications = (
                Publication.objects.filter(is_hidden=False).order_by('-pub_date').distinct()
            )
    publication_page = create_page(request, publications)
    tag_list = Tag.objects.all()
    context = {
        'publication_page': publication_page,
        'tag_list': tag_list,
    }
    return render(
        request,
        'pages/index.html',
        context,
    )


def user_page(request, user_id):
    if user_id == request.user.id:
        return redirect('pages:my_publications')
    author = get_object_or_404(User, id=user_id)
    publications = (
        Publication.objects.filter(author__username=author, is_hidden=False).order_by('-pub_date')
    )
    publication_page = create_page(request, publications)
    context = {
        'author': author,
        'publication_page': publication_page,
    }
    return render(request, 'pages/user_page.html', context)


def publication_page(request, publication_id):
    publication = get_object_or_404(Publication, pk=publication_id)
    user = request.user
    like = False
    if Like.objects.filter(user=user.id, publication=publication.id).exists():
        if getattr(get_object_or_404(Like, user=user.id, publication=publication.id), 'value')>= 1.0:
            like = True
    elif user != publication.author:
        Like.objects.get_or_create(
            user=user,
            publication=publication,
            value = 0.1,
        )
    if publication.is_hidden:
        comment = get_object_or_404(Comment, publication=publication)
        context = {
            'publication': publication,
            'like': like,
            'comment': comment,
            'show': 2,
        }
    elif user.is_moderator:
        form = CreateComment(request.POST or None) 
        context = {
            'publication': publication,
            'like': like,
            'form': form,
            'show': 1,
        }
    else:
        context = {
            'publication': publication,
            'like': like,
            'show': 0,
        }
    return render(request, 'pages/publication_page.html', context)


@login_required
def personal_page(request):
    author = get_object_or_404(User, id=request.user.id)
    tzinfo = datetime.timezone(datetime.timedelta(hours=3.0))
    if 120 <= datetime.datetime.now(tzinfo).hour*60 + datetime.datetime.now(tzinfo).minute < 780: 
        publications = (
            Publication.objects.filter(rec1__user=author, is_hidden=False).order_by('-rec1__value')
        )
    else:
        publications = (
            Publication.objects.filter(rec2__user=author, is_hidden=False).order_by('-rec2__value')
        )
    publication_page = create_page(request, publications)
    context = {
        'author': author,
        'publication_page': publication_page,
    }
    return render(request, 'pages/personal_page.html', context)


@login_required
def favorites(request):
    author = get_object_or_404(User, id=request.user.id)
    publications = (
        Publication.objects.filter(likes__user=author, is_hidden=False).order_by('-pub_date')
    )
    publication_page = create_page(request, publications)
    context = {
        'author': author,
        'publication_page': publication_page,
    }
    return render(request, 'pages/favorites.html', context)


@login_required
def my_publications(request):
    author = get_object_or_404(User, id=request.user.id)
    publications = (
        Publication.objects.filter(author__username=author).order_by('-pub_date')
    )
    publication_page = create_page(request, publications)
    context = {
        'author': author,
        'publication_page': publication_page,
    }
    return render(request, 'pages/my_publications.html', context)


@login_required
def create(request):
    form = PublicationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_publication = form.save(commit=False)
            username = request.user
            new_publication.author = username
            new_publication.save()
            return redirect('pages:index')
    return render(
        request,
        'pages/create.html',
        {'form': form}
    )


@login_required
def change(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    if request.user != publication.author:
        return HttpResponseNotFound()
    form = PublicationForm(
        request.POST or None,
        instance=publication
    )
    if request.method == 'POST':
        if form.is_valid():
            changed_publication = form.save()
            if Comment.objects.filter(publication=publication_id).exists():
                Comment.objects.filter(publication=publication_id).delete()
                changed_publication.is_hidden = False
                changed_publication.save()
            return redirect('pages:publication_page', publication_id=publication_id)
    return render(
        request,
        'pages/change.html',
        {'form': form, 'publication': publication}
    )


def moderation(request):
    if not request.user.is_moderator:
        return HttpResponseNotFound()
    publications = (
        Publication.objects.filter(is_hidden=True).order_by('-pub_date')
    )
    publication_page = create_page(request, publications)
    return render(
        request,
        'pages/moderation.html',
        {'publication_page': publication_page,}
    )


def create_comment(request, publication_id):
    if not request.user.is_moderator or request.method != 'POST':
        return HttpResponseNotFound()
    form = CreateComment(request.POST or None)
    publication = get_object_or_404(Publication, id=publication_id)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.publication = publication
        publication.is_hidden = True
        publication.save()
        new_comment.save()
    return redirect('pages:publication_page', publication_id=publication_id)


@login_required
def like(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    author = request.user
    like = get_object_or_404(Like, user=author.id, publication=publication.id)
    if getattr(like, 'value') < 1:
        like.value = 1.0
        like.save()
        return redirect('pages:publication_page', publication_id=publication_id)
    like.value = 0
    like.save()
    return redirect('pages:index')


class SignUp(CreateView):
    form_class = CreateUserForm
    template_name = 'users/signup.html'

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect('pages:index')
