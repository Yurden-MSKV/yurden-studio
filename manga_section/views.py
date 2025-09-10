from django.http import Http404
from decimal import Decimal

from manga_section.models import Manga, Chapter, ChapterImage, ChapterLike

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required


def manga_page(request, slug):
    # Получаем мангу с предзагрузкой всех связанных данных
    manga = get_object_or_404(Manga.objects.prefetch_related(
        'volumes__chapters__likes',
        'volumes__chapters__likes__user',
        'genres',
        'authors'
    ), manga_slug=slug)

    # Получаем тома, отсортированные по номеру
    volumes = manga.volumes.all().order_by('vol_number')

    # Передаем текущего пользователя в каждую главу
    for volume in volumes:
        for chapter in volume.chapters.all():
            chapter._current_user = request.user

    genres = manga.genres.all()
    authors = manga.authors.all()

    context = {
        'manga': manga,
        'volumes': volumes,
        'genres': genres,
        'authors': authors,
        'user': request.user,  # Добавляем пользователя в контекст
    }
    return render(request, 'manga_page.html', context)


@login_required
def chapter_like(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)

    try:
        data = json.loads(request.body)
        action = data.get('action')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    like, created = ChapterLike.objects.get_or_create(
        user=request.user,
        chapter=chapter,
    )

    if action == 'like':
        if like.is_like is True:
            like.is_like = None
        else:
            like.is_like = True
    elif action == 'dislike':
        if like.is_like is False:
            like.is_like = None
        else:
            like.is_like = False
    else:
        return JsonResponse({'error': 'Invalid action'}, status=400)

    like.save()

    # Пересчитываем счетчики
    like_count = chapter.likes.filter(is_like=True).count()
    dislike_count = chapter.likes.filter(is_like=False).count()
    total = like_count + dislike_count

    like_percentage = round((like_count / total) * 100) if total > 0 else 0
    dislike_percentage = round((dislike_count / total) * 100) if total > 0 else 0

    return JsonResponse({
        'like_count': like_count,
        'dislike_count': dislike_count,
        'like_percentage': like_percentage,
        'dislike_percentage': dislike_percentage,
        'user_reaction': like.is_like,
    })


def chapter_page(request, manga_slug, ch_number):
    # Ищем мангу по slug
    manga = get_object_or_404(Manga, manga_slug=manga_slug)

    # Преобразуем chapter_number в Decimal для поиска
    try:
        chapter_number_decimal = Decimal(ch_number)
    except:
        raise Http404("Неверный формат номера главы")

    chapter = get_object_or_404(
        Chapter.objects.filter(volume__manga=manga),
        ch_number=ch_number
    )

    images = ChapterImage.objects.filter(chapter=chapter).order_by('page_number')

    context = {
        'manga': manga,
        'chapter': chapter,
        'images': images,
    }
    return render(request, 'chapter_page.html', context)
