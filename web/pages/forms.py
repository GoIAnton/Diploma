from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django_summernote.fields import SummernoteWidget

from .models import Publication, Comment


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
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
                    'height': '300',
                },
            }),
        }

    def __init__(self, *args, **kwargs):
        super(PublicationForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['tags'].widget.attrs.update({'class': 'form-select'})


class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'text',
        )
        labels = {
            'text': 'Текст',
        }
    
    def __init__(self, *args, **kwargs):
        super(CreateComment, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
