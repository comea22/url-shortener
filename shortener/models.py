from django.db import models
from django.conf import settings

class ShortURL(models.Model):
    original_url = models.URLField(verbose_name='原網址')
    short_code = models.CharField(max_length=20, unique=True, verbose_name='縮網址代碼')
    password = models.CharField(max_length=50, blank=True, null=True, verbose_name='密碼')
    note = models.TextField(blank=True, null=True, verbose_name='備註說明')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

    def get_short_url(self):
        return f"{settings.SHORTENER_BASE_URL}{self.short_code}"

# Create your models here.
