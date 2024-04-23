import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apply_app.models import Application

class Shartnoma(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Foydalanuvchi')
    )
    apply = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        verbose_name=_('Ariza'),
        related_name='shartnoma'
    )
    shartnoma_fayl = models.FileField(
        upload_to='shartnomalar/',
        null=True,
        blank=True,
        verbose_name=_('Shartnoma fayli')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaratilgan vaqti')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yangilangan vaqti')
    )

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.apply.id}"

    class Meta:
        verbose_name = _('Shartnoma')
        verbose_name_plural = _('Shartnomalar')
