from django.shortcuts import render, get_object_or_404
from post_section.models import Post


def post_page(request, post_slug):
    post = get_object_or_404(Post, post_slug=post_slug)

    context = {
        'post': post,
    }

    session_key = f'article_{post.id}_viewed'

    if not request.session.get(session_key, False):
        # Если ключа нет — пользователь ещё не смотрел статью
        post.view_count += 1
        post.save()

        # Устанавливаем флаг, что пользователь уже смотрел
        request.session[session_key] = True

        # Устанавливаем время жизни сессии (5 минут)
        request.session.set_expiry(300)

    return render(request, 'post_page.html', context)