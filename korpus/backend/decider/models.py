from django.utils.timezone import now
from django.db import models
from reci.models import VRSTE_RECI, UserProxy


ODLUKE = [
    (1, 'без одлуке'),
    (2, 'иде у речник'),
    (3, 'не иде у речник'),
    (4, 'иде у проширени речник'),
    (5, 'уклонити из речника'),
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
    beleska = models.TextField('белешка', max_length=1000, blank=True)
    potkorpus_1 = models.BooleanField('поткорпус 1', default=False)
    potkorpus_2 = models.BooleanField('поткорпус 2', default=False)
    potkorpus_3 = models.BooleanField('поткорпус 3', default=False)
    potkorpus_4 = models.BooleanField('поткорпус 4', default=False)
    potkorpus_5 = models.BooleanField('поткорпус 5', default=False)
    potkorpus_6 = models.BooleanField('поткорпус 6', default=False)
    potkorpus_7 = models.BooleanField('поткорпус 7', default=False)
    potkorpus_8 = models.BooleanField('поткорпус 8', default=False)
    potkorpus_9 = models.BooleanField('поткорпус 9', default=False)

    class Meta:
        verbose_name = 'реч за одлуку'
        verbose_name_plural = 'речи за одлуку'
        indexes = [
            models.Index(fields=['prvo_slovo']),
            models.Index(fields=['tekst']),
            models.Index(fields=['recnik_id']),
            models.Index(fields=['korpus_id']),
            models.Index(fields=['broj_pojavljivanja']),
            models.Index(fields=['potkorpus_1']),
            models.Index(fields=['potkorpus_2']),
            models.Index(fields=['potkorpus_3']),
            models.Index(fields=['potkorpus_4']),
            models.Index(fields=['potkorpus_5']),
            models.Index(fields=['potkorpus_6']),
            models.Index(fields=['potkorpus_7']),
            models.Index(fields=['potkorpus_8']),
            models.Index(fields=['potkorpus_9']),
        ]
    
    def __str__(self) -> str:
        donosilac = str(self.donosilac_odluke.puno_ime()) if self.donosilac_odluke else '-'
        return f'{self.tekst} [{ODLUKE[self.odluka-1][1]}] : {str(self.vreme_odluke)} : {donosilac}' 


class DinamickiIzvestaj(models.Model):
    upit = models.CharField(max_length=1000)
    vreme_zahteva = models.DateTimeField('време захтева', default=now)
    vreme_pocetka = models.DateTimeField('време почетка', blank=True, null=True)
    vreme_zavrsetka = models.DateTimeField('време завршетка', blank=True, null=True)
    zavrsen = models.BooleanField('завршен', default=False)

    def __str__(self) -> str:
        return f'Динамички извештај {self.id}: {"завршен" if self.zavrsen else "није завршен"}'

