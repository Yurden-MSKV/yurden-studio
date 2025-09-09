from django.urls import path
from post_section import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<slug:post_slug>/', views.post_page, name='post-page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)