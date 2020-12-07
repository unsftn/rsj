# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from concurrency.fields import AutoIncVersionField


GLAGOLSKI_VID = [
    (0, 'непознат'),
    (1, 'свршени'),
    (2, 'несвршени'),
    (3, 'двовидски'),
]

GLAGOLSKI_ROD = [
    (0, 'непознат'),
    (1, 'прелазни'),
    (2, 'непрелазни'),
    (3, 'повратни'),
    (4, 'узајамно повратни'),
]

GLAGOLSKO_VREME = [
    (1, 'презент'),
    (2, 'футур 1'),
    (3, 'аорист'),
    (4, 'имперфекат'),
    (5, 'императив'),
]

ROD = [
    (1, 'мушки'),
    (2, 'женски'),
    (3, 'средњи'),
]

BROJ = [
    (1, 'једнина'),
    (2, 'множина'),
]

PADEZ = [
    (1, 'номинатив'),
    (2, 'генитив'),
    (3, 'датив'),
    (4, 'акузатив'),
    (5, 'вокатив'),
    (6, 'инструментал'),
    (7, 'локатив'),
]

PRIDEVSKI_VID = [
    (1, 'одређен'),
    (2, 'неодређен'),
    (3, 'компаратив'),
    (4, 'суперлатив'),
]


class VrstaImenice(models.Model):
    naziv = models.CharField('назив', max_length=100)

    def __str__(self):
        return self.naziv

    class Meta:
        verbose_name = 'врста именице'
        verbose_name_plural = 'врсте именица'


class Imenica(models.Model):
    vrsta = models.ForeignKey(VrstaImenice, verbose_name='врста именице', on_delete=models.DO_NOTHING)
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
    vreme = models.DateTimeField('време последње измене', default=now)
    version = AutoIncVersionField()

    def __str__(self):
        return self.nomjed if self.nomjed else '-'

    class Meta:
        verbose_name = 'именица'
        verbose_name_plural = 'именице'


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

    def __str__(self):
        return str(self.imenica) + ' / ' + (self.nomjed if self.nomjed else '-')

    class Meta:
        verbose_name = 'варијанта именице'
        verbose_name_plural = 'варијанте именица'


class IzmenaImenice(models.Model):
    imenica = models.ForeignKey(Imenica, verbose_name='именица', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време измене')

    def __str__(self):
        return str(self.imenica) + ' / ' + self.user.email + ' / ' + str(self.vreme)

    class Meta:
        verbose_name = 'измена именице'
        verbose_name_plural = 'измене именица'


class Glagol(models.Model):
    infinitiv = models.CharField('инфинитив', max_length=50, blank=True, null=True)
    vid = models.IntegerField('глаголски вид', choices=GLAGOLSKI_VID)
    rod = models.IntegerField('глаголски род', choices=GLAGOLSKI_ROD)
    rgp_mj = models.CharField('РГП муш јед', max_length=50, blank=True, null=True)
    rgp_zj = models.CharField('РГП жен јед', max_length=50, blank=True, null=True)
    rgp_sj = models.CharField('РГП сре јед', max_length=50, blank=True, null=True)
    rgp_mm = models.CharField('РГП муш мно', max_length=50, blank=True, null=True)
    rgp_zm = models.CharField('РГП жен мно', max_length=50, blank=True, null=True)
    rgp_sm = models.CharField('РГП сре мно', max_length=50, blank=True, null=True)
    gpp = models.CharField('ГПП', max_length=50, blank=True, null=True)
    gps = models.CharField('ГПС', max_length=50, blank=True, null=True)
    vreme = models.DateTimeField('време последње измене', default=now)
    version = AutoIncVersionField()

    def __str__(self):
        return self.infinitiv if self.infinitiv else '-'

    class Meta:
        verbose_name = 'глагол'
        verbose_name_plural = 'глаголи'


class OblikGlagola(models.Model):
    glagol = models.ForeignKey(Glagol, verbose_name='глагол', on_delete=models.CASCADE)
    vreme = models.IntegerField('глаголско време', choices=GLAGOLSKO_VREME)
    jd1 = models.CharField('прво лице једнине', max_length=50, blank=True, null=True)
    jd2 = models.CharField('друго лице једнине', max_length=50, blank=True, null=True)
    jd3 = models.CharField('треће лице једнине', max_length=50, blank=True, null=True)
    mn1 = models.CharField('прво лице множине', max_length=50, blank=True, null=True)
    mn2 = models.CharField('друго лице множине', max_length=50, blank=True, null=True)
    mn3 = models.CharField('треће лице множине', max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.glagol) + ' / ' + str(self.vreme) + ' / ' + self.jd1

    class Meta:
        verbose_name = 'облик глагола'
        verbose_name_plural = 'облици глагола'


class IzmenaGlagola(models.Model):
    glagol = models.ForeignKey(Glagol, verbose_name='глагол', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време измене')

    def __str__(self):
        return str(self.glagol) + ' / ' + self.user.email + ' / ' + str(self.vreme)

    class Meta:
        verbose_name = 'измена глагола'
        verbose_name_plural = 'измене глагола'


class Pridev(models.Model):
    tekst = models.CharField('текст', max_length=50, blank=True, null=True)
    vreme = models.DateTimeField('време последње измене', default=now)
    version = AutoIncVersionField()

    def __str__(self):
        return self.tekst if self.tekst else '-'

    class Meta:
        verbose_name = 'придев'
        verbose_name_plural = 'придеви'


class OblikPrideva(models.Model):
    pridev = models.ForeignKey(Pridev, verbose_name='придев', on_delete=models.CASCADE)
    tekst = models.CharField('текст', max_length=50, blank=True, null=True)
    vid = models.IntegerField('вид', choices=PRIDEVSKI_VID)
    rod = models.IntegerField('род', choices=ROD)
    broj = models.IntegerField('број', choices=BROJ)
    padez = models.IntegerField('падеж', choices=PADEZ)

    def __str__(self):
        return str(self.pridev) + ' / ' + self.tekst

    class Meta:
        verbose_name = 'облик придева'
        verbose_name_plural = 'облици придева'


class IzmenaPrideva(models.Model):
    pridev = models.ForeignKey(Pridev, verbose_name='придев', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време измене')

    def __str__(self):
        return str(self.pridev) + ' / ' + self.user.email + ' / ' + str(self.vreme)

    class Meta:
        verbose_name = 'измена придева'
        verbose_name_plural = 'измене придева'
