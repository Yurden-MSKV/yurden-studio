from django.http import Http404
from decimal import Decimal

from manga_section.models import Manga, Chapter, ChapterImage

from django.shortcuts import render, get_object_or_404


def manga_page(request, slug):
    # Получаем мангу с предзагрузкой всех связанных данных
    manga = get_object_or_404(Manga.objects.prefetch_related(
        'volumes__chapters',  # Тома и их главы
        'genres',
        'authors'
    ), manga_slug=slug)

    # Получаем тома, отсортированные по номеру
    volumes = manga.volumes.all().order_by('vol_number')

    genres = manga.genres.all()
    authors = manga.authors.all()

    context = {
        'manga': manga,
        'volumes': volumes,  # Добавляем тома в контекст
        'genres': genres,
        'authors': authors,
    }
    return render(request, 'manga_page.html', context)


def chapter_page(request, manga_slug, ch_number):
    # Ищем мангу по slug
    manga = get_object_or_404(Manga, manga_slug=manga_slug)

    # Преобразуем chapter_number в Decimal для поиска
    try:
        chapter_number_decimal = Decimal(ch_number)
    except:
        raise Http404("Неверный формат номера главы")

    # Ищем главу по номеру и связи с мангой
    chapter = get_object_or_404(
        Chapter,
        chapter_number=chapter_number_decimal,
        manga=manga
    )
    images = ChapterImage.objects.filter(chapter=chapter).order_by('page_number')

    context = {
        'manga': manga,
        'chapter': chapter,
        'images': images,
    }
    return render(request, 'chapter_page.html', context)
