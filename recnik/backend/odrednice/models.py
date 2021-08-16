# -*- coding: utf-8 -*-
from random import choices

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from concurrency.fields import AutoIncVersionField
from publikacije import models as publikacije_models

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
    (10, 'остало'),
]

STANJE_ODREDNICE = [
    (1, 'обрада лексикографа'),
    (2, 'обрада редактора'),
    (3, 'обрада уредника'),
    (4, 'завршена обрада'),
]

GLAGOLSKI_VID = [
    (1, 'свршени'),
    (2, 'несвршени'),
    (3, 'свршени и несвршени'),
    (4, 'несвршени и свршени'),
    (5, 'свршени (несвршени)'),
    (6, 'несвршени (свршени)'),
]

GLAGOLSKI_ROD = [
    (1, 'прелазни'),
    (2, 'непрелазни'),
    (3, 'повратни'),
    (4, 'прелазни и непрелазни'),
    (5, 'непрелазни и прелазни'),
    (6, '(се) облик'),
]

ROD = [
    (1, 'мушки'),
    (2, 'женски'),
    (3, 'средњи'),
    (4, 'мушки (женски)'),
    (5, 'женски (мушки)'),
    (6, 'мушки (средњи)'),
    (7, 'средњи (мушки)'),
    (8, 'женски (средњи)'),
    (9, 'средњи (женски)'),
    (10, 'мушки / женски'),
    (11, 'мушки / средњи'),
    (12, 'женски / средњи'),
]

TIP_GRAFIKONA = [
    (1, 'недељни принос'),
    (2, 'месечни принос'),
    (3, 'годишњи принос'),
    (4, 'недељни кумулативно'),
    (5, 'месечни кумулативно'),
    (6, 'годишњи кумулативно'),
]


class UserProxy(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' (' + self.email + ')'

    def puno_ime(self):
        return self.first_name + ' ' + self.last_name

    def je_obradjivac(self):
        return self._in_group(1)

    def je_redaktor(self):
        return self._in_group(2)

    def je_urednik(self):
        return self._in_group(3)

    def je_administrator(self):
        return self._in_group(4)

    def group_id(self):
        group = self.groups.all().first()
        if not group:
            return None
        return group.id

    def _in_group(self, group_id):
        group = self.groups.all().first()
        if not group:
            return False
        return group.id == group_id


class StatusOdrednice(models.Model):
    naziv = models.CharField('назив', max_length=50)

    def __str__(self):
        return self.naziv

    class Meta:
        verbose_name = 'статус одреднице'
        verbose_name_plural = 'статуси одредница'
        ordering = ['id']


class Odrednica(models.Model):
    rec = models.CharField('реч', max_length=50, blank=True, null=True)
    sortable_rec = models.CharField('реч за сортирање', max_length=50, blank=True, null=True)
    ijekavski = models.CharField('ијекавски', max_length=50, blank=True, null=True)
    vrsta = models.IntegerField('врста', choices=VRSTA_ODREDNICE)
    rod = models.IntegerField('род', choices=ROD, default=0, blank=True, null=True)
    nastavak = models.CharField('наставак', max_length=50, blank=True, null=True)
    nastavak_ij = models.CharField('наставак ијекавски', max_length=50, blank=True, null=True)
    info = models.CharField('инфо', max_length=2000, blank=True, null=True)
    glagolski_vid = models.IntegerField('глаголски вид', choices=GLAGOLSKI_VID, blank=True, null=True)
    glagolski_rod = models.IntegerField('глаголски род', choices=GLAGOLSKI_ROD, blank=True, null=True)
    prezent = models.CharField('презент', max_length=50, blank=True, null=True)
    prezent_ij = models.CharField('презент', max_length=50, blank=True, null=True)
    broj_pregleda = models.IntegerField('број прегледа', default=0)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)
    stanje = models.IntegerField('фаза обраде', choices=STANJE_ODREDNICE, default=1)
    opciono_se = models.BooleanField('опционо се', null=True, blank=True)
    version = AutoIncVersionField()
    rbr_homonima = models.PositiveSmallIntegerField('редни број хомонима', null=True, blank=True, default=None)
    obradjivac = models.ForeignKey(UserProxy, verbose_name='обрађивач', on_delete=models.PROTECT, related_name='odrednice_obradjivaca', default=1)
    redaktor = models.ForeignKey(UserProxy, verbose_name='редактор', on_delete=models.PROTECT, related_name='odrednice_redaktora', blank=True, null=True)
    urednik = models.ForeignKey(UserProxy, verbose_name='уредник', on_delete=models.PROTECT, related_name='odrednice_urednika', blank=True, null=True)
    napomene = models.TextField('напомене', max_length=2000, blank=True, null=True)
    freetext = models.TextField('алтернативни опис', max_length=2000, blank=True, null=True)
    status = models.ForeignKey(StatusOdrednice, verbose_name='статус одреднице', null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.rec if self.rec else '-'

    class Meta:
        verbose_name = 'одредница'
        verbose_name_plural = 'одреднице'
        indexes = [
            models.Index(fields=['rec']),
            models.Index(fields=['sortable_rec', 'rbr_homonima']),
            models.Index(fields=['poslednja_izmena'])
        ]

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
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.DO_NOTHING)
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
    nastavak_ij = models.CharField('наставак ијекавски', max_length=50, blank=True, null=True)
    prezent = models.CharField('презент', max_length=50, blank=True, null=True)
    prezent_ij = models.CharField('презент ијекавски', max_length=50, blank=True, null=True)
    opciono_se = models.BooleanField('опционо се', null=True, blank=True)
    rod = models.IntegerField('род', choices=ROD, default=0, blank=True, null=True)

    def __str__(self):
        return f'{str(self.odrednica)} / {self.redni_broj}: {self.tekst}'

    class Meta:
        verbose_name = 'варијанта одреднице'
        verbose_name_plural = 'варијанте одредница'
        ordering = ['redni_broj']
        indexes = [
            models.Index(fields=['redni_broj']),
        ]

    def get_absolute_url(self):
        return reverse('odrednice:izmena-varijante-detail', kwargs={'pk': self.pk})


class Antonim(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    ima_antonim = models.ForeignKey(Odrednica,  verbose_name='одредница има антоним', on_delete=models.CASCADE,
                                    related_name='ima_antonim')
    u_vezi_sa = models.ForeignKey(Odrednica, verbose_name='у вези са одредницом', on_delete=models.CASCADE,
                                  related_name='antonim_u_vezi_sa', null=True, blank=True)
    tekst = models.CharField('текст', max_length=100, blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'антоним'
        verbose_name_plural = 'антоними'
        ordering = ['redni_broj']
        indexes = [
            models.Index(fields=['redni_broj']),
        ]

    def __str__(self):
        return f'{self.redni_broj}: {self.ima_antonim.id} -> {self.u_vezi_sa.id if self.u_vezi_sa else self.tekst}'

    def get_absolute_url(self):
        return reverse("odrednice:antonim-detail", kwargs={"pk": self.pk})


class Sinonim(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    ima_sinonim = models.ForeignKey(Odrednica, verbose_name='одредница има синоним', on_delete=models.CASCADE,
                                    related_name='ima_sinonim')
    u_vezi_sa = models.ForeignKey(Odrednica, verbose_name='у вези са одредницом', on_delete=models.CASCADE,
                                  related_name='sinonim_u_vezi_sa', null=True, blank=True)
    tekst = models.CharField('текст', max_length=100, blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'синоним'
        verbose_name_plural = 'синоними'
        ordering = ['redni_broj']
        indexes = [
            models.Index(fields=['redni_broj']),
        ]

    def __str__(self):
        return f'{self.redni_broj}: {self.ima_sinonim.id} -> {self.u_vezi_sa.id if self.u_vezi_sa else self.tekst}'

    def get_absolute_url(self):
        return reverse("odrednice:sinonim-detail", kwargs={"pk": self.pk})


class Kolokacija(models.Model):
    napomena = models.CharField('напомена', max_length=2000, blank=True, null=True)
    odrednica = models.ForeignKey(Odrednica, verbose_name='одредница', on_delete=models.CASCADE)
    redni_broj = models.PositiveSmallIntegerField('редни број')

    class Meta:
        verbose_name = 'колокација'
        verbose_name_plural = 'колокације'
        ordering = ['redni_broj']
        indexes = [
            models.Index(fields=['redni_broj']),
        ]

    def __str__(self):
        return str(self.odrednica) + f'[{self.redni_broj}]'

    def get_absolute_url(self):
        return reverse("odrednice:kolokacija-detail", kwargs={"pk": self.pk})


class RecUKolokaciji(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    kolokacija = models.ForeignKey(Kolokacija, verbose_name='колокација', on_delete=models.CASCADE)
    odrednica = models.ForeignKey(Odrednica, verbose_name='одредница', on_delete=models.CASCADE, blank=True, null=True)
    tekst = models.CharField('текст', max_length=100, blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'реч у колокацији'
        verbose_name_plural = 'речи у колокацији'
        ordering = ['redni_broj']
        indexes = [
            models.Index(fields=['redni_broj']),
        ]

    def __str__(self):
        return f'{self.kolokacija.odrednica.rec}: {str(self.redni_broj)}'

    def get_absolute_url(self):
        return reverse("odrednice:rec-u-kolokaciji-detail", kwargs={"pk": self.pk})


class GrupaKvalifikatora(models.Model):
    skracenica = models.CharField('скраћеница', max_length=15)
    naziv = models.CharField('назив', max_length=50)
    nadgrupa = models.ForeignKey('self', verbose_name='надгрупа', blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'група квалификатора'
        verbose_name_plural = 'групе квалификатора'
        ordering = [models.functions.Collate('skracenica', 'utf8mb4_unicode_ci')]
        indexes = [
            models.Index(fields=['skracenica']),
        ]

    def __str__(self):
        return f'{self.skracenica}. / {self.naziv}'


class Kvalifikator(models.Model):
    skracenica = models.CharField('скраћеница', max_length=15)
    naziv = models.CharField('назив', max_length=50)
    grupa = models.ForeignKey(GrupaKvalifikatora, verbose_name='група', blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'квалификатор'
        verbose_name_plural = 'квалификатори'
        ordering = [models.functions.Collate('skracenica', 'utf8mb4_unicode_ci')]
        indexes = [
            models.Index(fields=['skracenica']),
        ]

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
        ordering = ['redni_broj']
        indexes = [
            models.Index(fields=['redni_broj']),
        ]

    def __str__(self):
        return str(self.redni_broj) + ': ' + str(self.kvalifikator)

    def get_absolute_url(self):
        return reverse("odrednice:kvalifikator-odrednice-detail", kwargs={"pk": self.pk})


class Znacenje(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    tekst = models.CharField('текст', max_length=2000, blank=True, null=True)
    odrednica = models.ForeignKey(Odrednica, verbose_name='одредница', on_delete=models.CASCADE)
    znacenje_se = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'значење'
        verbose_name_plural = 'значења'
        ordering = ['redni_broj', 'znacenje_se']
        indexes = [
            models.Index(fields=['redni_broj', 'znacenje_se']),
        ]

    def __str__(self):
        return str(self.odrednica) + ' / ' + str(self.redni_broj) + ': ' + self.tekst

    def get_absolute_url(self):
        return reverse("odrednice:znacenje-detail", kwargs={"pk": self.pk})


class KvalifikatorZnacenja(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    kvalifikator = models.ForeignKey(Kvalifikator, verbose_name='квалификатор', on_delete=models.CASCADE)
    znacenje = models.ForeignKey(Znacenje, verbose_name='значење', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'квалификатор значења'
        verbose_name_plural = 'квалификатори значења'
        ordering = ['redni_broj']
        indexes = [
            models.Index(fields=['redni_broj']),
        ]

    def __str__(self):
        return str(self.redni_broj) + ': ' + str(self.kvalifikator)

    def get_absolute_url(self):
        return reverse("odrednice:kvalifikator-znacenja-detail", kwargs={"pk": self.pk})


class Podznacenje(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    tekst = models.CharField('текст', max_length=2000)
    znacenje = models.ForeignKey(Znacenje, verbose_name='значење', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'подзначење'
        verbose_name_plural = 'подзначења'
        ordering = ['redni_broj']
        indexes = [
            models.Index(fields=['redni_broj']),
        ]

    def __str__(self):
        return str(self.znacenje.odrednica) + ' / ' + str(self.znacenje.redni_broj) + ' / ' + str(self.redni_broj) + \
               ' / ' + self.tekst

    def get_absolute_url(self):
        return reverse("odrednice:podznacenje-detail", kwargs={"pk": self.pk})


class KvalifikatorPodznacenja(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    kvalifikator = models.ForeignKey(Kvalifikator, verbose_name='квалификатор', on_delete=models.CASCADE)
    podznacenje = models.ForeignKey(Podznacenje, verbose_name='подзначење', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'квалификатор подзначења'
        verbose_name_plural = 'квалификатори подзначења'
        ordering = ['redni_broj']
        indexes = [
            models.Index(fields=['redni_broj']),
        ]

    def __str__(self):
        return str(self.redni_broj) + ': ' + str(self.kvalifikator)

    def get_absolute_url(self):
        return reverse("odrednice:kvalifikator-podznacenja-detail", kwargs={"pk": self.pk})


class IzrazFraza(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број', default=1)
    tekst = models.CharField('текст', max_length=200, default='', blank=True, null=True)
    opis = models.CharField('опис', max_length=2000, default='')
    odrednica = models.ForeignKey(Odrednica, verbose_name='припада одредници', blank=True, null=True, on_delete=models.CASCADE)
    znacenje = models.ForeignKey(Znacenje, verbose_name='значење', blank=True, null=True, on_delete=models.CASCADE)
    podznacenje = models.ForeignKey(Podznacenje, verbose_name='подзначење', blank=True, null=True, on_delete=models.CASCADE)
    vezana_odrednica = models.ForeignKey(Odrednica, verbose_name='везана одредница', blank=True, null=True, on_delete=models.CASCADE, related_name='vezana_odrednica')

    class Meta:
        verbose_name = 'израз фраза'
        verbose_name_plural = 'изрази фразе'
        ordering = ['redni_broj']
        indexes = [
            models.Index(fields=['redni_broj']),
        ]

    def __str__(self):
        return str(self.redni_broj) + ' ' + self.opis

    def get_absolute_url(self):
        return reverse("odrednice:izrazfraza-detail", kwargs={"pk": self.pk})


class Konkordansa(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    opis = models.CharField('опис', max_length=2000)
    znacenje = models.ForeignKey(Znacenje, verbose_name='значење', blank=True, null=True, on_delete=models.CASCADE)
    podznacenje = models.ForeignKey(Podznacenje, verbose_name='подзначење', blank=True, null=True, on_delete=models.CASCADE)
    izraz_fraza = models.ForeignKey(IzrazFraza, verbose_name='фраза', blank=True, null=True, on_delete=models.CASCADE)
    publikacija = models.ForeignKey(publikacije_models.Publikacija, verbose_name='публикација', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'конкорданса'
        verbose_name_plural = 'конкордансе'
        ordering = ['redni_broj']
        indexes = [
            models.Index(fields=['redni_broj']),
        ]

    def __str__(self):
        return str(self.redni_broj) + ' ' + self.opis

    def get_absolute_url(self):
        return reverse("odrednice:konkordansa-detail", kwargs={"pk": self.pk})


class KvalifikatorFraze(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    kvalifikator = models.ForeignKey(Kvalifikator, verbose_name='квалификатор', on_delete=models.CASCADE)
    izrazfraza = models.ForeignKey(IzrazFraza, verbose_name='израз фраза', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'квалификатор фразе'
        verbose_name_plural = 'квалификатори фраза'
        ordering = ['redni_broj']

    def __str__(self):
        return str(self.redni_broj) + ': ' + str(self.kvalifikator)

    def get_absolute_url(self):
        return reverse("odrednice:kvalifikator-fraze-detail", kwargs={"pk": self.pk})


class KolokacijaZnacenja(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    znacenje = models.ForeignKey(Znacenje, verbose_name='значење', on_delete=models.CASCADE)
    tekst = models.CharField('текст', max_length=2000, blank=True, null=True)

    class Meta:
        verbose_name = 'колокација значења'
        verbose_name_plural = 'колокације значења'
        ordering = ['redni_broj']
        indexes = [
            models.Index(fields=['redni_broj']),
        ]

    def __str__(self):
        return f'{str(self.znacenje)} [{self.redni_broj}] {self.tekst}'


class KolokacijaPodznacenja(models.Model):
    redni_broj = models.PositiveSmallIntegerField('редни број')
    podznacenje = models.ForeignKey(Podznacenje, verbose_name='значење', on_delete=models.CASCADE)
    tekst = models.CharField('текст', max_length=2000, blank=True, null=True)

    class Meta:
        verbose_name = 'колокација подзначења'
        verbose_name_plural = 'колокације подзначења'
        ordering = ['redni_broj']
        indexes = [
            models.Index(fields=['redni_broj']),
        ]

    def __str__(self):
        return f'{str(self.podznacenje)} [{self.redni_broj}] {self.tekst}'


class StatistikaUnosa(models.Model):
    vreme = models.DateTimeField('време генерисања')

    class Meta:
        verbose_name = 'статистика уноса'
        verbose_name_plural = 'статистике уноса'
        ordering = ['-vreme']
        indexes = [
            models.Index(fields=['vreme']),
        ]

    def __str__(self):
        return str(self.vreme)


class StavkaStatistikeUnosa(models.Model):
    statistika = models.ForeignKey(StatistikaUnosa, verbose_name='статистика', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.PROTECT)
    broj_odrednica = models.IntegerField('сачуваних одредница')
    broj_znakova = models.IntegerField('сачуваних знакова')
    zavrsenih_odrednica = models.IntegerField('завршених одредница', default=0)
    zavrsenih_znakova = models.IntegerField('завршених знакова', default=0)

    class Meta:
        verbose_name = 'ставка статистике уноса'
        verbose_name_plural = 'ставке статистике уноса'

    def __str__(self):
        return str(self.statistika) + ' / ' + self.user.first_name + ' ' + self.user.last_name


class GrafikonUnosa(models.Model):
    tip = models.IntegerField('тип графикона', choices=TIP_GRAFIKONA)
    vreme = models.DateTimeField('време генерисања', default=now)
    data = models.TextField('подаци')
    chart = models.TextField('графикон')

    class Meta:
        verbose_name = 'графикон уноса'
        verbose_name_plural = 'графикони уноса'

    def __str__(self):
        return f'{str(self.tip)} / {self.vreme.strftime("%Y-%m-%d %H:%M")}'
