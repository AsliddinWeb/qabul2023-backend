from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from auth_app.models import Passport
from course_app.models import Filial, TalimTuri, TalimShakli, Yonalish
from diplom_app.models import Diplom, PerevodDiplom


class ApplyStatus(models.Model):
    nomi = models.CharField(max_length=255, verbose_name=_("Holat nomi"))

    def __str__(self):
        return self.nomi


class Application(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='application',
        verbose_name=_("Foydalanuvchi")
    )
    passport = models.ForeignKey(
        Passport,
        on_delete=models.CASCADE,
        verbose_name=_("Pasport")
    )

    diplom = models.ForeignKey(
        Diplom,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Diplom")
    )
    perevod_diplom = models.ForeignKey(
        PerevodDiplom,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Diplomni o'tkazish")
    )
    is_perevod = models.BooleanField(
        default=False,
        verbose_name=_("Perevodmi?")
    )

    filial = models.ForeignKey(
        Filial,
        on_delete=models.CASCADE,
        verbose_name=_("Filial")
    )
    talim_turi = models.ForeignKey(
        TalimTuri,
        on_delete=models.CASCADE,
        verbose_name=_("Ta'lim turi")
    )
    talim_shakli = models.ForeignKey(
        TalimShakli,
        on_delete=models.CASCADE,
        verbose_name=_("Ta'lim shakli")
    )
    yonalish = models.ForeignKey(
        Yonalish,
        on_delete=models.CASCADE,
        verbose_name=_("Yo'nalish")
    )

    apply_status = models.ForeignKey(
        ApplyStatus,
        on_delete=models.CASCADE,
        verbose_name=_("Ariza holati")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Yaratilgan vaqti")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Yangilangan vaqti")
    )

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.apply_status.nomi}"
