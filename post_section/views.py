from django.shortcuts import render, get_object_or_404
from post_section.models import Post


def post_page(request, post_slug):
    post = get_object_or_404(Post, post_slug=post_slug)

    context = {
        'post': post,
    }

    # Проверяем, есть ли куки, что пользователь уже просматривал этот пост
    viewed_key = f'viewed_post_{post.id}'
    if not request.COOKIES.get(viewed_key):
        # Увеличиваем счетчик просмотров
        post.view_count += 1
        post.save()

        # Устанавливаем куки на 5 минут (300 секунд)
        response = render(request, 'post_page.html', {'post': post})
        response.set_cookie(viewed_key, 'true', max_age=300)
        return response

    return render(request, 'post_page.html', context)