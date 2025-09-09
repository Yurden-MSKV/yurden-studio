from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django import forms
from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import models
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from manga_section.models import (Genre, Manga, Author, Chapter, ChapterImage)


# Кастомный виджет для множественной загрузки файлов
class MultipleFileInput(forms.FileInput):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['multiple'] = 'multiple'
        super().__init__(attrs)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return None


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre_name']
    search_fields = ['genre_name']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['author_name']
    search_fields = ['author_name']


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1
    fields = ['ch_number', 'ch_name', 'edit_link']
    readonly_fields = ['edit_link']

    def edit_link(self, obj):
        if obj and obj.pk:
            url = reverse('admin:manga_site_chapter_change', args=[obj.pk])
            return format_html('<a href="{}">⚙️ Редактировать главу</a>', url)
        return "Сначала сохраните главу"

    edit_link.short_description = 'Действия'


class ChapterImageForm(forms.ModelForm):
    class Meta:
        model = ChapterImage
        fields = ['page_number', 'page_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['page_number'].required = False


class ChapterImageInline(admin.TabularInline):
    model = ChapterImage
    form = ChapterImageForm
    extra = 1
    fields = ['page_number', 'page_image', 'preview']
    readonly_fields = ['preview']
    verbose_name = 'Изображение страницы'
    verbose_name_plural = 'Изображения страниц'

    def preview(self, obj):
        if obj.page_image and hasattr(obj.page_image, 'url'):
            return format_html('<img src="{}" height="100" />', obj.page_image.url)
        return "Нет изображения"

    preview.short_description = 'Предпросмотр'


@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = ['manga_name', 'get_genres', 'get_authors', 'cover']
    filter_horizontal = ['genres', 'authors']
    search_fields = ['manga_name']

    def get_genres(self, obj):
        if obj.genres.exists():
            return ", ".join([genre.genre_name for genre in obj.genres.all()])
        return "Жанры не указаны"

    get_genres.short_description = 'Жанры'

    def get_authors(self, obj):
        if obj.authors.exists():
            return ", ".join([author.author_name for author in obj.authors.all()])
        return "Автор не указан"

    get_authors.short_description = 'Авторы'


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['get_manga_name', 'ch_number', 'ch_name']
    list_filter = ['manga']
    search_fields = ['ch_number', 'ch_name']

    # Добавляем кастомный шаблон для массовой загрузки
    change_form_template = 'admin/manga_section/chapter_change_form.html'

    def get_manga_name(self, obj):
        return obj.manga.manga_name

    get_manga_name.short_description = 'Манга'

    inlines = [ChapterImageInline]

    def response_change(self, request, obj):
        """Обрабатываем массовую загрузку изображений"""
        if 'upload_images' in request.POST:
            # Обрабатываем загруженные файлы
            files = request.FILES.getlist('images')
            if files:
                # Получаем следующий номер страницы
                existing_pages = ChapterImage.objects.filter(chapter=obj)
                if existing_pages.exists():
                    next_page_number = existing_pages.aggregate(
                        models.Max('page_number')
                    )['page_number__max'] + 1
                else:
                    next_page_number = 1

                # Сохраняем все файлы
                success_count = 0
                for i, file in enumerate(files):
                    try:
                        ChapterImage.objects.create(
                            chapter=obj,
                            page_number=next_page_number + i,
                            page_image=file
                        )
                        success_count += 1
                    except Exception as e:
                        messages.error(request, f'Ошибка при загрузке файла {file.name}: {str(e)}')

                if success_count > 0:
                    messages.success(request, f'Успешно загружено {success_count} изображений')

            return HttpResponseRedirect(request.path)

        return super().response_change(request, obj)