from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Tag, Like, Recommendation1, Recommendation2, User, Comment

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('full_text',)

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Recommendation1)
admin.site.register(Recommendation2)