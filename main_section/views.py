from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods

from main_section.forms import RegisterForm
from manga_section.models import Chapter, Volume
from post_section.models import Post


def index(request):
    return render(request, 'top_panel.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home-page')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

@require_http_methods(["GET"])
def custom_logout(request):
    logout(request)
    return redirect('login')  # или другой нужный вам URL


def main_page(request):
    last_week = timezone.now() - timezone.timedelta(days=7)

    # Оптимизируем запросы с prefetch_related для получения последних томов
    recent_chapters = Chapter.objects.filter(
        add_date__gte=last_week
    ).select_related(
        'volume__manga'
    ).prefetch_related(
        Prefetch('volume__manga__volumes',
                 queryset=Volume.objects.order_by('-vol_number'),
                 to_attr='latest_volumes')
    ).order_by('-add_date')

    recent_posts = Post.objects.filter(add_date__gte=last_week, visibility=True).order_by('-add_date')

    manga_dict = {}
    for chapter in recent_chapters:
        manga = chapter.volume.manga
        if manga.id not in manga_dict:
            # Получаем обложку последнего тома
            latest_volume = manga.volumes.order_by('-vol_number').first()
            cover = latest_volume.vol_cover if latest_volume else None

            manga_dict[manga.id] = {
                'manga': manga,
                'cover': cover,
                'chapters': []
            }
        manga_dict[manga.id]['chapters'].append(chapter)

    context = {
        'recent_manga': list(manga_dict.values()),
        'recent_post': recent_posts
    }
    return render(request, 'main_page.html', context)

def info_page(request):
    post = get_object_or_404(Post, post_slug='info')

    context = {
        'post': post,
    }

    return render(request, 'post_page.html', context)
