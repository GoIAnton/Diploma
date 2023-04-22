from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'full_text',
            'tags',
        )
        labels = {'full_text': 'Текст поста', 'tags': '  Тэг'}
        help_texts = {
            'text': 'Текст новой статьи',
            'tags': 'Гэг'}
