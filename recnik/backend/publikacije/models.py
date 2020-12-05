import os
from django.db import models


class VrstaPublikacije(models.Model):
    naziv = models.CharField('назив', max_length=300)

    def __str__(self):
        return self.naziv

    class Meta:
        verbose_name = 'врста публикације'
        verbose_name_plural = 'врсте публикација'


class Publikacija(models.Model):
    naslov = models.CharField('наслов', max_length=300)
    naslov_izdanja = models.CharField('наслов издања', max_length=300, blank=True, null=True)
    vrsta = models.ForeignKey(VrstaPublikacije, verbose_name='врста', on_delete=models.DO_NOTHING)
    isbn = models.CharField('ISBN', max_length=13, blank=True, null=True)
    issn = models.CharField('ISSN', max_length=8, blank=True, null=True)
    izdavac = models.CharField('издавач', max_length=200, blank=True, null=True)
    godina = models.CharField('година', max_length=10, blank=True, null=True)
    volumen = models.CharField('годиште', max_length=10, blank=True, null=True)
    broj = models.CharField('број', max_length=10, blank=True, null=True)
    url = models.URLField('URL', max_length=500, blank=True, null=True)
    vreme_unosa = models.DateTimeField('време уноса')

    def __str__(self):
        return self.naslov

    class Meta:
        verbose_name = 'публикација'
        verbose_name_plural = 'публикације'


class Autor(models.Model):
    ime = models.CharField('име', max_length=50, blank=True, null=True)
    prezime = models.CharField('презиме', max_length=50)

    def __str__(self):
        return self.prezime + (self.ime if self.ime else '')

    class Meta:
        verbose_name = 'аутор'
        verbose_name_plural = 'аутори'


class AutorPublikacije(models.Model):
    publikacija = models.ForeignKey(Publikacija, verbose_name='публикација', on_delete=models.DO_NOTHING)
    autor = models.ForeignKey(Autor, verbose_name='аутор', on_delete=models.DO_NOTHING)
    redni_broj = models.PositiveSmallIntegerField('редни број')

    def __str__(self):
        return str(self.publikacija) + ' / ' + str(self.autor) + ' / ' + str(self.redni_broj)

    class Meta:
        verbose_name = 'аутор публикације'
        verbose_name_plural = 'аутори публикација'


class TekstPublikacije(models.Model):
    publikacija = models.ForeignKey(Publikacija, verbose_name='публикација', on_delete=models.DO_NOTHING)
    redni_broj = models.PositiveSmallIntegerField('редни број')
    tekst = models.TextField('текст')

    def __str__(self):
        return str(self.publikacija) + ': ' + str(self.redni_broj)

    class Meta:
        verbose_name = 'текст публикације'
        verbose_name_plural = 'текстови публикација'


def get_upload_path(instance, filename):
    return os.path.join('publikacije', str(instance.publikacija.id), str(instance.redni_broj))


class FajlPublikacije(models.Model):
    publikacija = models.ForeignKey(Publikacija, verbose_name='публикација', on_delete=models.DO_NOTHING)
    redni_broj = models.PositiveSmallIntegerField('редни број')
    uploaded_file = models.FileField('фајл', upload_to=get_upload_path)

    def __str__(self):
        return str(self.publikacija) + ': ' + str(self.redni_broj)

    class Meta:
        verbose_name = 'фајл публикације'
        verbose_name_plural = 'фајлови публикација'
