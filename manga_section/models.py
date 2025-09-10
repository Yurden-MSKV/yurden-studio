from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    genre_name = models.CharField(max_length=25,
                                  unique=True,
                                  verbose_name="Жанр")

    def __str__(self):
        return self.genre_name


class Author(models.Model):
    author_name = models.CharField(max_length=50,
                                   unique=True,
                                   verbose_name='Автор')

    def __str__(self):
        return self.author_name

    # def manga_cover_path(instance, filename):
    #     return f'manga/covers/{instance.id}/{filename}'


class Manga(models.Model):
    manga_name = models.CharField(max_length=150,
                                  verbose_name='Название')
    manga_slug = models.SlugField(max_length=200,
                                  verbose_name='SLUG-адрес',
                                  unique=True)
    genres = models.ManyToManyField(Genre,
                                    verbose_name='Жанр')
    authors = models.ManyToManyField(Author,
                                     verbose_name='Автор')
    description = models.TextField(verbose_name='Описание')

    def get_latest_volume_cover(self):
        # Получаем последний том по номеру (или по дате, если нужно)
        latest_volume = self.volumes.order_by('-vol_number').first()
        if latest_volume and latest_volume.vol_cover:
            return latest_volume.vol_cover
        return None

    def __str__(self):
        return self.manga_name


def volume_cover_path(instance, filename):
    return f'manga/volumes/covers/{instance.id}/{filename}'


class Volume(models.Model):
    manga = models.ForeignKey(Manga,
                              on_delete=models.CASCADE,
                              related_name='volumes',
                              verbose_name='Манга')
    vol_number = models.PositiveIntegerField(verbose_name='Номер тома')
    vol_cover = models.ImageField(upload_to=volume_cover_path)

    def __str__(self):
        return f'Том {str(self.vol_number)}'


class ChapterLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey('manga_section.Chapter', on_delete=models.CASCADE, related_name='likes')
    is_like = models.BooleanField(null=True, blank=True)  # True - лайк, False - дизлайк, None - нет оценки

    class Meta:
        unique_together = ('user', 'chapter')  # Один пользователь - одна оценка на главу

    def __str__(self):
        return f"{self.user.username}: {'Like' if self.is_like else 'Dislike'} on {self.chapter}"


class Chapter(models.Model):
    volume = models.ForeignKey(Volume,
                               on_delete=models.CASCADE,
                               related_name='chapters',
                               verbose_name='Том')
    ch_number = models.PositiveIntegerField(verbose_name='Номер')
    ch_name = models.CharField(max_length=100,
                               verbose_name='Название')
    add_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата и время создания')

    def __str__(self):
        return f'Глава {str(self.ch_number)}'

    def get_chapter_display(self):
        num = float(self.ch_number)
        if num.is_integer():
            return str(int(num))
        else:
            return str(num)

    # Добавляем свойства для оценок
    @property
    def like_count(self):
        return self.likes.filter(is_like=True).count()

    @property
    def dislike_count(self):
        return self.likes.filter(is_like=False).count()

    @property
    def total_votes(self):
        return self.like_count + self.dislike_count

    @property
    def like_percentage(self):
        if self.total_votes == 0:
            return 0
        return round((self.like_count / self.total_votes) * 100)

    @property
    def dislike_percentage(self):
        if self.total_votes == 0:
            return 0
        return round((self.dislike_count / self.total_votes) * 100)

    def get_user_reaction(self):
        """Получить реакцию пользователя (для использования в шаблоне)"""
        # Этот метод будет работать только если мы передали пользователя в главу
        if hasattr(self, '_current_user'):
            user = self._current_user
            if user.is_authenticated:
                try:
                    like = self.likes.get(user=user)
                    return like.is_like
                except:
                    return None
        return None


def chapter_image_path(instance, filename):
    return f'manga/chapters/images/{instance.chapter.id}/{filename}'


class ChapterImage(models.Model):
    chapter = models.ForeignKey(Chapter,
                                on_delete=models.CASCADE,
                                related_name='images')
    page_number = models.PositiveIntegerField(verbose_name='Номер страницы')
    page_image = models.ImageField(upload_to=chapter_image_path,  # Используем функцию
                                   verbose_name='Страница')
