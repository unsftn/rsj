from django.contrib import admin
from .models import (Odrednica, Antonim, Sinonim, Znacenje,
                     OperacijaIzmene, IzmenaOdrednice, Kolokacija, IzrazFraza,
                     RecUKolokaciji, Kvalifikator, KvalifikatorOdrednice,
                     Podznacenje, VarijantaOdrednice)


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
admin.site.register(Znacenje)
admin.site.register(Podznacenje)
admin.site.register(VarijantaOdrednice)
