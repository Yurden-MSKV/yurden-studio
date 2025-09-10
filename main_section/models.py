from django.contrib.auth.models import User
from django.db import models

from manga_section.models import Chapter


class ChapterLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,
                                related_name='likes')
    is_like = models.BooleanField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'chapter')

    def __str__(self):
        return f"{self.user.username}: {'Лайк' if self.is_like else 'Дизлайк'} главе {self.chapter.ch_name}"