from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class BlogUser(models.Model):
    user = models.OneToOneField(User, verbose_name="Usuário", on_delete=models.CASCADE)
    writer = models.BooleanField(default=False, verbose_name="Escritor")

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=30, verbose_name="Titulo", blank=False)
    content = models.TextField(verbose_name="Texto", blank=False)
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name="Autor")
    publish = models.BooleanField(verbose_name="Postado", default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(verbose_name="Slug", unique=True, default="", editable=False, max_length=50)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

class Comment(models.Model):
    email = models.EmailField(verbose_name="Email")
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name="Autor")
    content = models.TextField(verbose_name="Texto")
