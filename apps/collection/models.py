from django.db import models
from django.conf import settings
from apps.whisky.models import Whisky



class Collection(models.Model):
    # 내 장식장 - 마셔본 위스키
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='collections'
    )
    whisky = models.ForeignKey(
        Whisky,
        on_delete=models.CASCADE,
        related_name='collections'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'whisky')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.nickname} - {self.whisky.name}"
    

class Wishlist(models.Model):
    # 위시리스트 - 마시고 싶은 위스키
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wishlists'
    )
    whisky = models.ForeignKey(
        Whisky,
        on_delete=models.CASCADE,
        related_name='wishlists'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'whisky')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.nickname} - {self.whisky.name}"