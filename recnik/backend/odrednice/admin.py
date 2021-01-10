from django import forms
from django.contrib import admin
from .models import (Odrednica, Antonim, Sinonim, Znacenje,
                     OperacijaIzmene, IzmenaOdrednice, Kolokacija, IzrazFraza,
                     RecUKolokaciji, Kvalifikator, KvalifikatorOdrednice,
                     Podznacenje, VarijantaOdrednice)


class ZnacenjeForm(forms.ModelForm):
    tekst = forms.CharField(widget=forms.Textarea, max_length=2000, required=False)

    class Meta:
        model = Znacenje
        fields = '__all__'


class ZnacenjeAdmin(admin.ModelAdmin):
    form = ZnacenjeForm


class PodznacenjeForm(forms.ModelForm):
    tekst = forms.CharField(widget=forms.Textarea, max_length=2000)

    class Meta:
        model = Podznacenje
        fields = '__all__'


class PodznacenjeAdmin(admin.ModelAdmin):
    form = PodznacenjeForm


admin.site.register(Odrednica)
admin.site.register(OperacijaIzmene)
admin.site.register(IzmenaOdrednice)
admin.site.register(Antonim)
admin.site.register(Sinonim)
admin.site.register(Kolokacija)
admin.site.register(RecUKolokaciji)
admin.site.register(IzrazFraza)
admin.site.register(Kvalifikator)
admin.site.register(KvalifikatorOdrednice)
admin.site.register(Znacenje, ZnacenjeAdmin)
admin.site.register(Podznacenje, PodznacenjeAdmin)
admin.site.register(VarijantaOdrednice)
