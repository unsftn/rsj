# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

OPERACIJE_IZMENE = [
    (1, 'креирана реч'),
    (2, 'измењена реч'),
]

VRSTE_RECI = {
    0: 'именица',
    1: 'глагол',
    2: 'придев',
    3: 'прилог',
    4: 'предлог',
    5: 'заменица',
    6: 'узвик',
    7: 'речца',
    8: 'везник',
    9: 'број',
    10: 'остало',
}

VRSTE_IMENICA = [
    (1, 'апстрактна'),
    (2, 'заједничка'),
    (3, 'властита'),
    (4, 'збирна'),
    (5, 'градивна'),
    (6, 'глаголска'),
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
    (6, 'прелазни (непрелазни)'),
    (7, 'непрелазни (прелазни)'),
]

GLAGOLSKO_VREME = [
    (1, 'презент'),
    (2, 'футур 1'),
    (3, 'аорист'),
    (4, 'имперфекат'),
    (5, 'императив'),
]

OBLIK_GLAGOLSKE_VARIJANTE = [
    (1, 'пр.л.јед.'),
    (2, 'др.л.јед.'),
    (3, 'тр.л.јед.'),
    (4, 'пр.л.мн.'),
    (5, 'др.л.мн.'),
    (6, 'тр.л.мн.'),
]


def _append_attr(array, obj, attr_name):
    """
    Dodaje na kraj niza array vrednost atributa pod nazivom attr_name objekta obj, ako atribut i vrednost postoje
    """
    if hasattr(obj, attr_name):
        value = getattr(obj, attr_name)
        if value:
            array.append(value)


class UserProxy(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' (' + self.email + ')'

    def puno_ime(self):
        return self.first_name + ' ' + self.last_name


class StatusReci(models.Model):
    naziv = models.CharField('назив', max_length=50)

    def __str__(self):
        return self.naziv

    class Meta:
        verbose_name = 'статус речи'
        verbose_name_plural = 'статуси речи'
        ordering = ['id']


class Imenica(models.Model):
    nomjed = models.CharField('номинатив једнине', max_length=50)
    genjed = models.CharField('генитив једнине', max_length=50, blank=True, null=True)
    datjed = models.CharField('датив једнине', max_length=50, blank=True, null=True)
    akujed = models.CharField('акузатив једнине', max_length=50, blank=True, null=True)
    vokjed = models.CharField('вокатив једнине', max_length=50, blank=True, null=True)
    insjed = models.CharField('инструментал једнине', max_length=50, blank=True, null=True)
    lokjed = models.CharField('локатив једнине', max_length=50, blank=True, null=True)
    nommno = models.CharField('номинатив множине', max_length=50, blank=True, null=True)
    genmno = models.CharField('генитив множине', max_length=50, blank=True, null=True)
    datmno = models.CharField('датив множине', max_length=50, blank=True, null=True)
    akumno = models.CharField('акузатив множине', max_length=50, blank=True, null=True)
    vokmno = models.CharField('вокатив множине', max_length=50, blank=True, null=True)
    insmno = models.CharField('инструментал множине', max_length=50, blank=True, null=True)
    lokmno = models.CharField('локатив множине', max_length=50, blank=True, null=True)
    vrsta = models.IntegerField('врста именице', choices=VRSTE_IMENICA, blank=True, null=True)
    recnik_id = models.IntegerField('ID одреднице у речнику', blank=True, null=True)
    status = models.ForeignKey(StatusReci, verbose_name='статус речи', on_delete=models.PROTECT, blank=True, null=True)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)

    class Meta:
        verbose_name = 'именица'
        verbose_name_plural = 'именице'
        ordering = ['id']
        indexes = [
            models.Index(fields=['vrsta']),
            models.Index(fields=['nomjed'])
        ]

    def __str__(self):
        return f'{self.id}: {self.nomjed}'

    def oblici(self):
        retval = _svi_oblici_imenice(self)
        for var in self.varijantaimenice_set.all():
            retval.extend(_svi_oblici_imenice(var))
        return retval


class VarijantaImenice(models.Model):
    imenica = models.ForeignKey(Imenica, verbose_name='именица', on_delete=models.CASCADE)
    redni_broj = models.PositiveSmallIntegerField('редни број')
    nomjed = models.CharField('номинатив једнине', max_length=50, blank=True, null=True)
    genjed = models.CharField('генитив једнине', max_length=50, blank=True, null=True)
    datjed = models.CharField('датив једнине', max_length=50, blank=True, null=True)
    akujed = models.CharField('акузатив једнине', max_length=50, blank=True, null=True)
    vokjed = models.CharField('вокатив једнине', max_length=50, blank=True, null=True)
    insjed = models.CharField('инструментал једнине', max_length=50, blank=True, null=True)
    lokjed = models.CharField('локатив једнине', max_length=50, blank=True, null=True)
    nommno = models.CharField('номинатив множине', max_length=50, blank=True, null=True)
    genmno = models.CharField('генитив множине', max_length=50, blank=True, null=True)
    datmno = models.CharField('датив множине', max_length=50, blank=True, null=True)
    akumno = models.CharField('акузатив множине', max_length=50, blank=True, null=True)
    vokmno = models.CharField('вокатив множине', max_length=50, blank=True, null=True)
    insmno = models.CharField('инструментал множине', max_length=50, blank=True, null=True)
    lokmno = models.CharField('локатив множине', max_length=50, blank=True, null=True)


class IzmenaImenice(models.Model):
    imenica = models.ForeignKey(Imenica, verbose_name='именица', on_delete=models.CASCADE)
    operacija_izmene = models.PositiveSmallIntegerField('операција измене', choices=OPERACIJE_IZMENE)
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време', default=now)

    class Meta:
        verbose_name = 'измена именице'
        verbose_name_plural = 'измене именица'


def _svi_oblici_imenice(imenica):
    retval = []
    for x in ['nomjed', 'genjed', 'datjed', 'akujed', 'vokjed', 'insjed', 'lokjed', 'nommno', 'genmno', 'datmno',
              'akumno', 'vokmno', 'insmno', 'lokmno']:
        _append_attr(retval, imenica, x)
    return retval


class Glagol(models.Model):
    gl_rod = models.IntegerField('глаголски род', choices=GLAGOLSKI_ROD, blank=True, null=True)
    gl_vid = models.IntegerField('глаголски вид', choices=GLAGOLSKI_VID, blank=True, null=True)
    infinitiv = models.CharField('инфинитив', max_length=50, blank=True, null=True)
    rgp_mj = models.CharField('ргп м.јед.', max_length=50, blank=True, null=True)
    rgp_zj = models.CharField('ргп ж.јед.', max_length=50, blank=True, null=True)
    rgp_sj = models.CharField('ргп с.јед.', max_length=50, blank=True, null=True)
    rgp_mm = models.CharField('ргп м.мн.', max_length=50, blank=True, null=True)
    rgp_zm = models.CharField('ргп ж.мн.', max_length=50, blank=True, null=True)
    rgp_sm = models.CharField('ргп с.мн.', max_length=50, blank=True, null=True)
    gpp = models.CharField('гл.прил. прошли', max_length=50, blank=True, null=True)
    gps = models.CharField('гл.прил. садашњи', max_length=50, blank=True, null=True)
    recnik_id = models.IntegerField('ID одреднице у речнику', blank=True, null=True)
    status = models.ForeignKey(StatusReci, verbose_name='статус речи', on_delete=models.PROTECT, blank=True, null=True)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)

    class Meta:
        verbose_name = 'глагол'
        verbose_name_plural = 'глаголи'
        ordering = ['id']
        indexes = [
            models.Index(fields=['infinitiv']),
        ]

    def __str__(self):
        return f'{self.id}: {self.infinitiv}'

    def oblici(self):
        retval = []
        _append_attr(retval, self, 'infinitiv')
        retval.extend(_svi_oblici_glagola(self))
        return retval


class OblikGlagola(models.Model):
    glagol = models.ForeignKey(Glagol, verbose_name='глагол', on_delete=models.CASCADE)
    vreme = models.IntegerField('време', choices=GLAGOLSKO_VREME)
    jd1 = models.CharField('прво лице једнине', max_length=50, blank=True, null=True)
    jd2 = models.CharField('друго лице једнине', max_length=50, blank=True, null=True)
    jd3 = models.CharField('треће лице једнине', max_length=50, blank=True, null=True)
    mn1 = models.CharField('прво лице множине', max_length=50, blank=True, null=True)
    mn2 = models.CharField('друго лице множине', max_length=50, blank=True, null=True)
    mn3 = models.CharField('треће лице множине', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'глаголски облик'
        verbose_name_plural = 'глаголски облици'
        ordering = ['id']
        indexes = [
            models.Index(fields=['jd1']),
        ]

    def __str__(self):
        return f'{self.glagol.id}: {self.vreme}: {self.jd1}'


class VarijanteGlagola(models.Model):
    oblik_glagola = models.ForeignKey(OblikGlagola, verbose_name='облик глагола', on_delete=models.CASCADE)
    varijanta = models.IntegerField('варијанта', choices=OBLIK_GLAGOLSKE_VARIJANTE)
    tekst = models.CharField('текст', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'варијанта глагола'
        verbose_name_plural = 'варијанте глагола'
        ordering = ['id']

    def __str__(self):
        return f'{self.oblik_glagola.glagol.id}: {self.oblik_glagola.vreme}: {self.tekst}'


class IzmenaGlagola(models.Model):
    glagol = models.ForeignKey(Glagol, verbose_name='глагол', on_delete=models.CASCADE)
    operacija_izmene = models.PositiveSmallIntegerField('операција измене', choices=OPERACIJE_IZMENE)
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време', default=now)

    class Meta:
        verbose_name = 'измена глагола'
        verbose_name_plural = 'измене глагола'


def _svi_oblici_glagola(glagol):
    retval = []
    for oblik in glagol.oblikglagola_set.all():
        for x in ['jd1', 'jd2', 'jd3', 'mn1', 'mn2', 'mn3']:
            _append_attr(retval, oblik, x)
        for var in oblik.varijanteglagola_set.all():
            _append_attr(retval, var, 'tekst')
    return retval
