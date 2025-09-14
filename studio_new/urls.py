"""
URL configuration for studio_new project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from main_section import views as main_section_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_section_views.index),
    path('home/', main_section_views.main_page, name='home-page'),
    path('manga/', include('manga_section.urls')),
    path('post/', include('post_section.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('register/', main_section_views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', main_section_views.custom_logout, name='logout'),
    path('info/', main_section_views.info_page, name='info'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
