from django.db import models

# User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        default=None,
    )

    def __str__(self):
        return self.slug


class Post(models.Model):
    title = models.CharField(
        max_length=200,
    )
    full_text = models.TextField()
    tags = models.ManyToManyField(
        Tag,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.title
