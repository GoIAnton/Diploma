from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django_summernote.fields import SummernoteWidget

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'full_text',
            'tags',
            'is_article',
        )
        labels = {
            'full_text': 'Текст',
            'tags': 'Теги',
            'title': 'Название',
            'is_article': 'Это статья?'
        }
        help_texts = {
            'title': "Название должно быть уникальным",
            'tags': "Удерживайте 'Control' (или 'Command' на Mac), чтобы выбрать несколько значений.",
        }
        widgets = {
            'full_text': SummernoteWidget(attrs={
                'summernote': {
                    'airMode': False,
                    'width': '100%',
                    'height': '1000',
                },
            }),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['tags'].widget.attrs.update({'class': 'form-select'})


class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
        )


class AddComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'post',
            'text',
        )
        labels = {
            'post': 'Id новости или статьи',
            'text': 'Текст',
        }
    
    def __init__(self, *args, **kwargs):
        super(AddComment, self).__init__(*args, **kwargs)
        self.fields['post'].widget.attrs.update({'class': 'form-select'})
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
