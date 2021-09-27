# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


OPERACIJE_IZMENE = [
    (1, 'креирана реч'),
    (2, 'измењена реч'),
]

VRSTE_IMENICA = [
    (1, 'апстрактна'),
    (2, 'заједничка'),
    (3, 'властита'),
    (4, 'збирна'),
    (5, 'градивна'),
    (6, 'глаголска'),
]


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
    vrsta = models.IntegerField('врста именице', choices=VRSTE_IMENICA, null=True)
    recnik_id = models.IntegerField('ID одреднице у речнику', null=True)
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
