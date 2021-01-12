# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from korpus import models as korpus_models
from concurrency.fields import AutoIncVersionField
from django.urls import reverse

VRSTA_ODREDNICE = [
    (0, 'именица'),
    (1, 'глагол'),
    (2, 'придев'),
    (3, 'прилог'),
    (4, 'предлог'),
    (5, 'заменица'),
    (6, 'узвик'),
    (7, 'речца'),
    (8, 'везник'),
    (9, 'број'),
]

STANJE_ODREDNICE = [
    (1, 'обрада лексикографа'),
    (2, 'обрада редактора'),
    (3, 'обрада уредника'),
    (4, 'завршена обрада'),
]


class Odrednica(models.Model):
    rec = models.CharField('реч', max_length=50, blank=True, null=True)
    ijekavski = models.CharField('ијекавски', max_length=50, blank=True, null=True)
    vrsta = models.IntegerField('врста', choices=VRSTA_ODREDNICE)
    rod = models.IntegerField('род', choices=korpus_models.ROD, default=0, blank=True, null=True)
    nastavak = models.CharField('наставак', max_length=50, blank=True, null=True)
    info = models.CharField('инфо', max_length=2000, blank=True, null=True)
    glagolski_vid = models.IntegerField('глаголски вид', choices=korpus_models.GLAGOLSKI_VID, blank=True, null=True)
    glagolski_rod = models.IntegerField('глаголски род', choices=korpus_models.GLAGOLSKI_ROD, blank=True, null=True)
    prezent = models.CharField('презент', max_length=50, blank=True, null=True)
    broj_pregleda = models.IntegerField('број прегледа', default=0)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)
    stanje = models.IntegerField('стање', choices=STANJE_ODREDNICE, default=1)
    version = AutoIncVersionField()

    def __str__(self):
        return self.rec if self.rec else '-'

    class Meta:
        verbose_name = 'одредница'
        verbose_name_plural = 'одреднице'

    def get_absolute_url(self):
        return reverse("odrednice:odrednica-detail",
                       kwargs={"pk": self.pk})


class OperacijaIzmene(models.Model):
    naziv = models.CharField('назив', max_length=50)

    def __str__(self):
        return self.naziv

    class Meta:
        verbose_name = 'операција измене одреднице'
        verbose_name_plural = 'операције измена одредница'

    def get_absolute_url(self):
        return reverse("odrednice:operacija-izmene-detail", kwargs={"pk": self.pk})


class IzmenaOdrednice(models.Model):
    odrednica = models.ForeignKey(Odrednica, verbose_name='одредница', on_delete=models.CASCADE)
    operacija_izmene = models.ForeignKey(OperacijaIzmene, verbose_name='операција измене одреднице',
                                         on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време', default=now)

    class Meta:
        verbose_name = 'измена одреднице'
        verbose_name_plural = 'измене одредница'

    def __str__(self):
        return str(self.odrednica) \
            + ' / ' + self.user.email \
            + ' / ' + str(self.vreme)

    def get_absolute_url(self):
        return reverse("odrednice:izmena-odrednice-detail", kwargs={"pk": self.pk})


class VarijantaOdrednice(models.Model):
    odrednica = models.ForeignKey(Odrednica, verbose_name='одредница', on_delete=models.CASCADE)
    ijekavski = models.CharField('ијекавски', max_length=50, blank=True, null=True)
    redni_broj = models.PositiveSmallIntegerField('редни број')
    tekst = models.CharField('текст', max_length=50)
    nastavak = models.CharField('наставак', max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{str(self.odrednica)} / {self.redni_broj}: {self.tekst}'

    class Meta:
        verbose_name = 'варијанта одреднице'
        verbose_name_plural = 'варијанте одредница'

    def get_absolute_url(self):
        return reverse('odrednice:izmena-varijante-detail', kwargs={'pk': self.pk})


class Antonim(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    ima_antonim_id = models.ForeignKey(Odrednica,  verbose_name='одредница има антоним', on_delete=models.CASCADE,
                                       related_name='ima_antonim')
    u_vezi_sa_id = models.ForeignKey(Odrednica, verbose_name='у вези са одредницом', on_delete=models.CASCADE,
                                     related_name='antonim_u_vezi_sa')

    def get_absolute_url(self):
        return reverse("odrednice:antonim-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'антоним'
        verbose_name_plural = 'антоними'

    def __str__(self):
        return str(self.ima_antonim_id)


class Sinonim(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    ima_sinonim_id = models.ForeignKey(Odrednica, verbose_name='одредница има синоним', on_delete=models.CASCADE,
                                       related_name='ima_sinonim')
    u_vezi_sa_id = models.ForeignKey(Odrednica, verbose_name='у вези са одредницом', on_delete=models.CASCADE,
                                     related_name='sinonim_u_vezi_sa')

    class Meta:
        verbose_name = 'синоним'
        verbose_name_plural = 'синоними'

    def __str__(self):
        return str(self.ima_sinonim_id)

    def get_absolute_url(self):
        return reverse("odrednice:sinonim-detail", kwargs={"pk": self.pk})


class Kolokacija(models.Model):
    napomena = models.CharField('напомена', max_length=2000)
    odrednica = models.ForeignKey(Odrednica, verbose_name='одредница', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'колокација'
        verbose_name_plural = 'колокације'

    def __str__(self):
        return str(self.odrednica)

    def get_absolute_url(self):
        return reverse("odrednice:kolokacija-detail", kwargs={"pk": self.pk})


class RecUKolokaciji(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    kolokacija = models.ForeignKey(Kolokacija, verbose_name='колокација', on_delete=models.CASCADE)
    odrednica = models.ForeignKey(Odrednica, verbose_name='одредница', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'реч у колокацији'
        verbose_name_plural = 'речи у колокацији'

    def __str__(self):
        return str(self.redni_broj)

    def get_absolute_url(self):
        return reverse("odrednice:rec-u-kolokaciji-detail", kwargs={"pk": self.pk})


class IzrazFraza(models.Model):
    opis = models.CharField('опис', max_length=2000)
    u_vezi_sa = models.ForeignKey(Odrednica, verbose_name='у вези са одредницом',  on_delete=models.CASCADE,
                                  related_name="izrazfraza_u_vezi_sa")
    pripada_odrednici = models.ForeignKey(Odrednica, verbose_name='одредница', on_delete=models.CASCADE,
                                          related_name='pripada_odrednici')

    class Meta:
        verbose_name = 'израз фраза'
        verbose_name_plural = 'изрази фразе'

    def __str__(self):
        return str(self.pripada_odrednici_id)

    def get_absolute_url(self):
        return reverse("odrednice:izrazfraza-detail", kwargs={"pk": self.pk})


class Kvalifikator(models.Model):
    skracenica = models.CharField('скраћеница', max_length=15)
    naziv = models.CharField('назив', max_length=50)

    class Meta:
        verbose_name = 'квалификатор'
        verbose_name_plural = 'квалификатори'

    def __str__(self):
        return f'{self.skracenica}. / {self.naziv}'

    def get_absolute_url(self):
        return reverse("odrednice:kvalifikator-detail", kwargs={"pk": self.pk})


class KvalifikatorOdrednice(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    kvalifikator = models.ForeignKey(Kvalifikator, verbose_name='квалификатор', on_delete=models.CASCADE)
    odrednica = models.ForeignKey(Odrednica, verbose_name='одредница', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'квалификатор одреднице'
        verbose_name_plural = 'квалификатори одредница'

    def __str__(self):
        return str(self.redni_broj) + ': ' + str(self.kvalifikator)

    def get_absolute_url(self):
        return reverse("odrednice:kvalifikator-odrednice-detail", kwargs={"pk": self.pk})


class Znacenje(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    tekst = models.CharField('текст', max_length=2000, blank=True, null=True)
    odrednica = models.ForeignKey(Odrednica, verbose_name='одредница', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'значење'
        verbose_name_plural = 'значења'

    def __str__(self):
        return str(self.odrednica) + ' / ' + str(self.redni_broj) + ': ' + self.tekst

    def get_absolute_url(self):
        return reverse("odrednice:znacenje-detail", kwargs={"pk": self.pk})


class Podznacenje(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    tekst = models.CharField('текст', max_length=2000)
    znacenje = models.ForeignKey(Znacenje, verbose_name='значење', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'подзначење'
        verbose_name_plural = 'подзначења'

    def __str__(self):
        return str(self.znacenje.odrednica) + ' / ' + str(self.znacenje.redni_broj) + ' / ' + str(self.redni_broj) + \
               ' / ' + self.tekst

    def get_absolute_url(self):
        return reverse("odrednice:podznacenje-detail", kwargs={"pk": self.pk})
