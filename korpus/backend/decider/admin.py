from django.contrib import admin
from .models import *

class RecZaOdlukuAdmin(admin.ModelAdmin):
    list_display = ['tekst', 'vreme_odluke', 'donosilac_odluke']
    list_filter = ['odluka', ('donosilac_odluke', admin.RelatedOnlyFieldListFilter)]

admin.site.register(GenerisaniSpisak)
admin.site.register(RecZaOdluku, RecZaOdlukuAdmin)
