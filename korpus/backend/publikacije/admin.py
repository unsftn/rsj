from django.contrib import admin
from .models import *


class VrstaPublikacijeAdmin(admin.ModelAdmin):
    list_display = ['naziv']


class PublikacijaAdmin(admin.ModelAdmin):
    list_display = ['naslov', 'izdavac', 'godina']
    list_filter = ['izdavac']


class TekstPublikacijeAdmin(admin.ModelAdmin):
    list_display = ['publikacija', 'redni_broj']
    list_filter = ['publikacija__naslov']


admin.site.register(VrstaPublikacije, VrstaPublikacijeAdmin)
admin.site.register(Publikacija, PublikacijaAdmin)
admin.site.register(Autor)
admin.site.register(TekstPublikacije, TekstPublikacijeAdmin)
