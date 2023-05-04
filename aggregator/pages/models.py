from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE = (
        (MODERATOR, MODERATOR),
        (USER, USER)
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE,
        default=USER,
    )

    @property
    def is_admin(self):
        return self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER



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
        unique=True,
    )
    full_text = models.TextField()
    tags = models.ManyToManyField(
        Tag,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    is_article = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    value = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_follow',
            )
        ]


class Recommendation1(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='rec1',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rec1',
    )
    value = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )


class Recommendation2(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='rec2',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rec2',
    )
    value = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )
