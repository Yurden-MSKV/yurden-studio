from django.shortcuts import render
from django.utils import timezone

from manga_section.models import Chapter
from post_section.models import Post

def index(request):
    return render(request, 'top_panel.html')


def main_page(request):
    last_week = timezone.now() - timezone.timedelta(days=7)

    # Оптимизируем запросы с select_related и prefetch_related
    recent_chapters = Chapter.objects.filter(
        add_date__gte=last_week
    ).select_related(
        'manga'
    ).order_by('-add_date')

    recent_posts = Post.objects.filter(
        add_date__gte=last_week
    ).order_by('-add_date')

    # Группируем в памяти без дополнительных запросов
    manga_dict = {}

    for chapter in recent_chapters:
        manga = chapter.manga
        if manga.id not in manga_dict:
            manga_dict[manga.id] = {
                'manga': manga,
                'chapters': []
            }
        manga_dict[manga.id]['chapters'].append(chapter)

    context = {
        'recent_manga': list(manga_dict.values()),
        'recent_post': recent_posts
    }
    return render(request, 'main_page.html', context)
