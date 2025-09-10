from django.db import models


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


class Chapter(models.Model):
    volume = models.ForeignKey(Volume,
                              on_delete=models.CASCADE,
                              related_name='chapters',
                              verbose_name='Манга')
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


def chapter_image_path(instance, filename):
    return f'manga/chapters/images/{instance.chapter.id}/{filename}'


class ChapterImage(models.Model):
    chapter = models.ForeignKey(Chapter,
                                on_delete=models.CASCADE,
                                related_name='images')
    page_number = models.PositiveIntegerField(verbose_name='Номер страницы')
    page_image = models.ImageField(upload_to=chapter_image_path,  # Используем функцию
                                   verbose_name='Страница')
