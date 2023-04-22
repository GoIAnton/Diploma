from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Tag

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('full_text',)

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)