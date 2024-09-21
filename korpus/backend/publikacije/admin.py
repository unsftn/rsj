from django.contrib import admin
from .models import *


class VrstaPublikacijeAdmin(admin.ModelAdmin):
    list_display = ['naziv']


class PublikacijaAdmin(admin.ModelAdmin):
    list_display = ['naslov', 'izdavac', 'godina']
    list_filter = ['izdavac', 'potkorpus']


class TekstPublikacijeAdmin(admin.ModelAdmin):
    list_display = ['publikacija', 'redni_broj']


class FajlPublikacijeAdmin(admin.ModelAdmin):
    list_display = ['publikacija', 'redni_broj', 'filename']


admin.site.register(VrstaPublikacije, VrstaPublikacijeAdmin)
admin.site.register(Publikacija, PublikacijaAdmin)
admin.site.register(Autor)
admin.site.register(TekstPublikacije, TekstPublikacijeAdmin)
admin.site.register(FajlPublikacije, FajlPublikacijeAdmin)
admin.site.register(Potkorpus)
