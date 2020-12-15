# -*- coding: utf-8 -*-
import os
from django.db import models


class TipRenderovanogDokumenta(models.Model):
    naziv = models.CharField('назив', max_length=200)

    def __str__(self):
        return self.naziv

    class Meta:
        verbose_name = 'тип рендерованог документа'
        verbose_name_plural = 'типови рендерованог документа'


def get_rendered_file_path(instance, filename):
    return os.path.join('renderi', str(instance.tip_dokumenta.id), str(instance.id)+'.pdf')


class RenderovaniDokument(models.Model):
    tip_dokumenta = models.ForeignKey(TipRenderovanogDokumenta, verbose_name='тип документа',
                                      on_delete=models.DO_NOTHING)
    vreme_rendera = models.DateTimeField()
    opis = models.CharField('опис', max_length=100)
    rendered_file = models.FileField('фајл', upload_to=get_rendered_file_path)
    napomena = models.TextField()

    def __str__(self):
        return str(self.tip_dokumenta) + ' / ' + str(self.vreme_rendera)

    class Meta:
        verbose_name = 'рендеровани документ'
        verbose_name_plural = 'рендеровани документи'
