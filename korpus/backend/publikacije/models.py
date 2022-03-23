import os
from django.db import models
from django.utils.timezone import now
from reci.models import UserProxy
from .processing import FILTER_CHOICES


class VrstaPublikacije(models.Model):
    naziv = models.CharField('назив', max_length=300)

    def __str__(self):
        return self.naziv

    class Meta:
        verbose_name = 'врста публикације'
        verbose_name_plural = 'врсте публикација'


class Potkorpus(models.Model):
    naziv = models.CharField('назив', max_length=300)

    def __str__(self):
        return self.naziv

    class Meta:
        verbose_name = 'поткорпус'
        verbose_name_plural = 'поткорпуси'


class Publikacija(models.Model):
    naslov = models.CharField('наслов', max_length=300)
    naslov_izdanja = models.CharField('наслов издања', max_length=300, blank=True, null=True)
    vrsta = models.ForeignKey(VrstaPublikacije, verbose_name='врста', on_delete=models.DO_NOTHING, blank=True, null=True)
    isbn = models.CharField('ISBN', max_length=13, blank=True, null=True)
    issn = models.CharField('ISSN', max_length=8, blank=True, null=True)
    izdavac = models.CharField('издавач', max_length=200, blank=True, null=True)
    godina = models.CharField('година', max_length=10, blank=True, null=True)
    volumen = models.CharField('годиште', max_length=10, blank=True, null=True)
    broj = models.CharField('број', max_length=10, blank=True, null=True)
    url = models.URLField('URL', max_length=500, blank=True, null=True)
    vreme_unosa = models.DateTimeField('време уноса', default=now)
    potkorpus = models.ForeignKey(Potkorpus, verbose_name='поткорпус', on_delete=models.PROTECT, blank=True, null=True)
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.DO_NOTHING)
    skracenica = models.CharField('скраћеница', max_length=100, default='-')

    def __str__(self):
        return self.naslov

    class Meta:
        verbose_name = 'публикација'
        verbose_name_plural = 'публикације'


class Autor(models.Model):
    publikacija = models.ForeignKey(Publikacija, verbose_name='публикација', on_delete=models.DO_NOTHING)
    ime = models.CharField('име', max_length=50, blank=True, null=True)
    prezime = models.CharField('презиме', max_length=50)
    redni_broj = models.PositiveSmallIntegerField('редни број')

    def __str__(self):
        return str(self.publikacija) + ' / ' + \
               self.prezime + (' ' + self.ime if self.ime else '') + ' / ' \
               + str(self.redni_broj)

    class Meta:
        verbose_name = 'аутор'
        verbose_name_plural = 'аутори'


class TekstPublikacije(models.Model):
    publikacija = models.ForeignKey(Publikacija, verbose_name='публикација', on_delete=models.DO_NOTHING)
    redni_broj = models.PositiveSmallIntegerField('редни број')
    tekst = models.TextField('текст', blank=True)
    tagovan_tekst = models.TextField('тагован текст', blank=True)

    def __str__(self):
        return str(self.publikacija) + ': ' + str(self.redni_broj)

    class Meta:
        verbose_name = 'текст публикације'
        verbose_name_plural = 'текстови публикација'
        ordering = ['redni_broj']
        indexes = [
            models.Index(fields=['redni_broj'])
        ]


def get_upload_path(instance, filename):
    return os.path.join('publikacije', str(instance.publikacija.id), filename)


class FajlPublikacije(models.Model):
    publikacija = models.ForeignKey(Publikacija, verbose_name='публикација', on_delete=models.DO_NOTHING)
    redni_broj = models.PositiveSmallIntegerField('редни број')
    uploaded_file = models.FileField('фајл', upload_to=get_upload_path)

    def __str__(self):
        return str(self.publikacija) + ': ' + str(self.redni_broj)

    def filename(self):
        return os.path.basename(self.uploaded_file.name)

    def filepath(self):
        return self.uploaded_file.path

    def url(self):
        return self.uploaded_file.url

    class Meta:
        verbose_name = 'фајл публикације'
        verbose_name_plural = 'фајлови публикација'
        ordering = ['redni_broj']


class FilterPublikacije(models.Model):
    publikacija = models.ForeignKey(Publikacija, verbose_name='публикација', on_delete=models.CASCADE)
    redni_broj = models.PositiveSmallIntegerField('редни број')
    vrsta_filtera = models.IntegerField('врста филтера', choices=FILTER_CHOICES)

    def __str__(self):
        return f'{str(self.publikacija)}: {self.redni_broj}: {self.vrsta_filtera}'

    class Meta:
        verbose_name = 'филтер публикације'
        verbose_name_plural = 'филтери публикација'
        ordering = ['redni_broj']


class ParametarFiltera(models.Model):
    filter = models.ForeignKey(FilterPublikacije, verbose_name='публикација', on_delete=models.CASCADE)
    redni_broj = models.PositiveSmallIntegerField('редни број')
    naziv = models.CharField('назив', max_length=30)
    vrednost = models.CharField('vrednost', max_length=1000, blank=True, null=True)

    def __str__(self):
        return f'{str(self.filter)}: {self.redni_broj}: {self.naziv}: {self.vrednost}'

    class Meta:
        verbose_name = 'параметар филтера'
        verbose_name_plural = 'параметри филтера'
        ordering = ['redni_broj']
