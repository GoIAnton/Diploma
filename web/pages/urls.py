from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = 'pages'

urlpatterns = [
    path(
        'publication/<int:publication_id>/like/',
        views.like,
        name='like',
    ),
    path(
        'publication/<int:publication_id>/create_comment/',
        views.create_comment,
        name='create_comment',
    ),
    path(
        'publication/<int:publication_id>/',
        views.publication_page,
        name='publication_page',
    ),
    path(
        'personal_page/',
        views.personal_page,
        name='personal_page',
    ),
    path(
        'favorites/',
        views.favorites,
        name='favorites',
    ),
    path(
        'my_publications/',
        views.my_publications,
        name='my_publications',
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
        'change/<int:publication_id>/',
        views.change,
        name='change',
    ),
    path(
        'moderation/',
        views.moderation,
        name='moderation',
    ),
    path('signup/',
        views.SignUp.as_view(),
        name='signup'
    ),
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
    path('', views.index, name='index'),
]
