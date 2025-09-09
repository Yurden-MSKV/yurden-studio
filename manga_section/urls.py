from django.urls import path
from manga_section import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<slug:slug>/', views.manga_page, name='manga-page'),
    path('<slug:manga_slug>/chapter/<str:ch_number>/', views.chapter_page, name='chapter-page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)