from django.db import models

class Filial(models.Model):
    nomi = models.CharField(max_length=100, verbose_name="Filial nomi")

    def __str__(self):
        return self.nomi

# Bakalavr, Magistratura
class TalimTuri(models.Model):
    nomi = models.CharField(max_length=100, verbose_name="Ta'lim turi nomi")

    def __str__(self):
        return self.nomi

# Kunduzgi, sirtqi
class TalimShakli(models.Model):
    nomi = models.CharField(max_length=100, verbose_name="Ta'lim shakli nomi")

    def __str__(self):
        return self.nomi

class Yonalish(models.Model):
    nomi = models.CharField(max_length=200, verbose_name="Yo'nalish nomi")

    filial = models.ForeignKey(Filial, on_delete=models.CASCADE)
    talim_turi = models.ForeignKey(TalimTuri, on_delete=models.CASCADE)
    talim_shakli = models.ForeignKey(TalimShakli, on_delete=models.CASCADE)

    kontrakt_narxi = models.CharField(max_length=455, verbose_name="Kontrakt narxi")
    yonalish_kodi = models.CharField(max_length=255)
    oqish_muddati = models.CharField(max_length=255)
    shartnoma_seriyasi = models.CharField(max_length=255, verbose_name="Shartnoma seriyasi")

    def __str__(self):
        return self.nomi

class RegisterSlayder(models.Model):
    image = models.ImageField(upload_to='register-slayder/')
    title = models.CharField(max_length=455)
    body = models.TextField()
    button_text = models.CharField(max_length=455)

    def __str__(self):
        return self.title
