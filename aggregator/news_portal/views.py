from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Post, Tag
from django.http import HttpResponse

def create_page_obj(request, post_list):
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    tag = request.GET.get("tag", 0)
    post_list = (
        Post.objects.order_by('-pub_date')
    )
    page_obj = create_page_obj(request, post_list)
    tag_list = Tag.objects.all()
    context = {
        'page_obj': page_obj,
        'tag_list': tag_list,
    }
    return render(
        request,
        'news_and_posts/index.html',
        context,
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)
