from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from apps.whisky.models import Whisky


class TastingNote(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasting_notes'
    )
    whisky = models.ForeignKey(
        Whisky,
        on_delete=models.CASCADE,
        related_name='tasting_notes'
    )

    tags = models.JSONField(default=list, blank=True)
    # 유저 자유 입력, 태그당 20자 이내 / 최대 10개
    note = models.TextField(blank=True)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)]
        )
    # 0.5 단위, 5.0 만점

    is_public = models.BooleanField(default=True)
    tasted_at = models.DateField(default=date.today)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-tasted_at']

    def __str__(self):
        return f"{self.user.nickname} - {self.whisky.name} ({self.tasted_at})"