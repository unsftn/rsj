from django.contrib import admin
from .models import *


class PublikacijaAdmin(admin.ModelAdmin):
    list_display = ('naslov', 'naslov_izdanja', 'izdavac', 'godina', 'volumen', 'broj')
    search_fields = ('id', 'naslov', 'naslov_izdanja', 'godina', 'izdavac')
    list_filter = ('naslov_izdanja', 'izdavac', 'godina')


admin.site.register(VrstaPublikacije)
admin.site.register(Publikacija, PublikacijaAdmin)
admin.site.register(Autor)
admin.site.register(TekstPublikacije)
admin.site.register(FajlPublikacije)
