from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import re


class Post(models.Model):
    post_name = models.CharField(max_length=150,
                                 verbose_name='Название')
    post_slug = models.SlugField(max_length=200,
                                 unique=True,
                                 verbose_name='SLUG-адрес')
    content = RichTextUploadingField(verbose_name='Содержание')
    add_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата и время создания')
    view_count = models.PositiveIntegerField(default=0,
                                             editable=False,
                                             verbose_name='Счётчик просмотров')

    def __str__(self):
        return self.post_name

    def get_short_content(self, max_length=115):
        """
        Возвращает укороченное содержимое без изображений и с заменой &nbsp; на пробелы
        """
        # Удаляем все теги img
        content_no_images = re.sub(r'<img[^>]*>', '', self.content)

        # Заменяем &nbsp; на обычные пробелы
        content_no_nbsp = re.sub(r'&nbsp;', ' ', content_no_images)

        # Получаем чистый текст
        text_only = re.sub(r'<[^>]*>', '', content_no_nbsp)

        # Обрезаем текст
        if len(text_only) > max_length:
            return text_only[:max_length] + '...'
        return text_only

    def get_short_content_safe(self, max_length=115):
        """
        Безопасная версия для использования в шаблонах
        """
        from django.utils.safestring import mark_safe
        return mark_safe(self.get_short_content(max_length))