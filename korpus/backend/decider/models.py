from django.db import models
from reci.models import VRSTE_RECI, UserProxy


ODLUKE = [
    (1, 'без одлуке'),
    (2, 'иде у речник'),
    (3, 'не иде у речник'),
    (4, 'уклонити из речника'),
]


class GenerisaniSpisak(models.Model):
    start_time = models.DateTimeField('почетак генерисања', auto_now=True)
    end_time = models.DateTimeField('крај генерисања', blank=True, null=True)

    class Meta:
        verbose_name = 'генерисани списак речи'
        verbose_name_plural = 'генерисани спискови речи'


class RecZaOdluku(models.Model):
    prvo_slovo = models.CharField('прво слово', max_length=1)
    tekst = models.CharField('текст', max_length=100)
    vrsta_reci = models.IntegerField('врста речи', choices=VRSTE_RECI.items(), blank=True, null=True)
    korpus_id = models.IntegerField('ID речи у корпусу', blank=True, null=True)
    recnik_id = models.IntegerField('ID речи у речнику', blank=True, null=True)
    odluka = models.IntegerField('одлука', choices=ODLUKE)
    broj_publikacija = models.IntegerField('број публикација')
    broj_pojavljivanja = models.IntegerField('број појављивања')
    poslednje_generisanje = models.ForeignKey(GenerisaniSpisak, verbose_name='последње генерисање', on_delete=models.PROTECT)
    vreme_odluke = models.DateTimeField('време одлуке')
    donosilac_odluke = models.ForeignKey(UserProxy, verbose_name='доносилац одлуке', blank=True, null=True, on_delete=models.PROTECT)
    beleska = models.TextField('белешка', blank=True)

    class Meta:
        verbose_name = 'реч за одлуку'
        verbose_name_plural = 'речи за одлуку'
        indexes = [
            models.Index(fields=['prvo_slovo']),
            models.Index(fields=['tekst']),
            models.Index(fields=['beleska']),
            models.Index(fields=['recnik_id']),
            models.Index(fields=['korpus_id']),
        ]
