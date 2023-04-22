from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'posts/<int:post_id>/',
        views.post_detail,
        name='post_detail',
    ),
    path(
        'article_create',
        views.article_create,
        name='article_create',
    ),
]
