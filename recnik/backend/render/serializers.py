import logging
from rest_framework import serializers
from .models import *

log = logging.getLogger(__name__)


class TipRenderovanogDokumentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipRenderovanogDokumenta
        fields = ('id', 'naziv')


class RenderovaniDokumentSerializer(serializers.ModelSerializer):
    tip_dokumenta = TipRenderovanogDokumentaSerializer()

    class Meta:
        model = RenderovaniDokument
        fields = ('id', 'vreme_rendera', 'opis', 'napomena', 'rendered_file', 'tip_dokumenta', 'file_type')
