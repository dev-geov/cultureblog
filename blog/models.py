from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from .constants import CHARS


class BlogUser(models.Model):
    user = models.OneToOneField(User, verbose_name="Usuário", on_delete=models.CASCADE)
    writer = models.BooleanField(default=False, verbose_name="Escritor")

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(verbose_name="Slug", unique=True, default="", editable=False, max_length=30)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        for letter in value:
            if letter in 'õãàáéíóúç':
                value = value.replace(letter, CHARS.get(letter))
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)



class Post(models.Model):
    title = models.CharField(max_length=30, verbose_name="Titulo", blank=False)
    content = models.TextField(verbose_name="Texto", blank=False)
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name="Autor")
    publish = models.BooleanField(verbose_name="Postado", default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(verbose_name="Slug", unique=True, default="", editable=False, max_length=50)
    category = models.ManyToManyField(Category, verbose_name="Categoria")

    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.title
        for letter in value:
            if letter in 'ãõàáéíóúç':
                value = value.replace(letter, CHARS.get(letter))
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="Email")
    content = models.TextField(verbose_name="Texto")
