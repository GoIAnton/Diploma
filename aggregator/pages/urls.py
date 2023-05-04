from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'posts/<int:post_id>/',
        views.post_page,
        name='post_page',
    ),
    path(
        'users/<int:user_id>/',
        views.user_page,
        name='user_page',
    ),
    path(
        'create/',
        views.create,
        name='create',
    ),
    path(
        'moderation/',
        views.moderation,
        name='moderation',
    ),
    path(
        'posts/<int:post_id>/like/',
        views.like,
        name='like',
    ),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
]
