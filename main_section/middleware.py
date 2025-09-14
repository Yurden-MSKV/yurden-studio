# middleware.py
from django.shortcuts import redirect
from django.urls import reverse


class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URL, которые доступны без авторизации
        public_urls = [
            reverse('login'),
            reverse('register'),
            reverse('logout'),
            '/admin/login/',
            # добавьте другие публичные URL
        ]

        if not request.user.is_authenticated and request.path not in public_urls:
            return redirect('login')

        return self.get_response(request)