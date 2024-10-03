from django.db import models
from django.utils.text import slugify
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    slug = models.CharField(max_length=200, unique=True)
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog_previews/', **NULLABLE, verbose_name='превью (изображение)')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='дата создания')
    is_published = models.BooleanField(default=False, verbose_name='признак публикации')
    views = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блог-пост'
        verbose_name_plural = 'блог-посты'
        permissions = [
            ("add_post", "Can add post"),
            ("change_post", "Can change post"),
            ("delete_post", "Can delete post"),
        ]

