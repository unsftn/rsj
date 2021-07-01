# -*- coding: utf-8 -*-
import os
from django.db import models
from odrednice.models import StatusOdrednice

FILE_TYPES = [
    (1, 'pdf'),
    (2, 'docx'),
]


class TipRenderovanogDokumenta(models.Model):
    naziv = models.CharField('назив', max_length=200)
    statusi = models.ManyToManyField(StatusOdrednice)

    def __str__(self):
        return self.naziv

    class Meta:
        verbose_name = 'тип рендерованог документа'
        verbose_name_plural = 'типови рендерованог документа'


def get_rendered_file_path(instance, filename):
    return os.path.join('renderi', str(instance.tip_dokumenta.id), str(instance.id)+f'.{(FILE_TYPES[instance.file_type-1])[1]}')


class RenderovaniDokument(models.Model):
    tip_dokumenta = models.ForeignKey(TipRenderovanogDokumenta, verbose_name='тип документа',
                                      on_delete=models.DO_NOTHING)
    vreme_rendera = models.DateTimeField()
    opis = models.CharField('опис', max_length=100)
    rendered_file = models.FileField('фајл', upload_to=get_rendered_file_path)
    napomena = models.TextField()
    file_type = models.PositiveSmallIntegerField('тип фајла', choices=FILE_TYPES, default=1)

    def __str__(self):
        return str(self.tip_dokumenta) + ' / ' + str(self.vreme_rendera)

    class Meta:
        verbose_name = 'рендеровани документ'
        verbose_name_plural = 'рендеровани документи'
        indexes = [
            models.Index(fields=['vreme_rendera']),
        ]
