from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Kvalifikator, Odrednica, VarijantaOdrednice
from .text import remove_punctuation, remove_hyphens


@receiver(post_save, sender=Kvalifikator)
def sync_kvalifikator_to_memory(sender, instance, created, raw, using, update_fields, **kwargs):
    if created and using == 'default':
        instance.save(using='memory')


@receiver(pre_save, sender=Odrednica)
def clean_odrednica(sender, instance, raw, using, update_fields, **kwargs):
    instance.rec = remove_hyphens(instance.rec)
    instance.ijekavski = remove_hyphens(instance.ijekavski)
    instance.prezent = remove_hyphens(instance.prezent)
    instance.prezent_ij = remove_hyphens(instance.prezent_ij)
    instance.nastavak = remove_hyphens(instance.nastavak)
    instance.nastavak_ij = remove_hyphens(instance.nastavak_ij)
    instance.freetext = remove_hyphens(instance.freetext)
    instance.info = remove_hyphens(instance.info)
    instance.sortable_rec = remove_punctuation(instance.rec)


@receiver(pre_save, sender=VarijantaOdrednice)
def clean_varijanta(sender, instance, raw, using, update_fields, **kwargs):
    instance.tekst = remove_hyphens(instance.tekst)
    instance.ijekavski = remove_hyphens(instance.ijekavski)
    instance.prezent = remove_hyphens(instance.prezent)
    instance.prezent_ij = remove_hyphens(instance.prezent_ij)
    instance.nastavak = remove_hyphens(instance.nastavak)
    instance.nastavak_ij = remove_hyphens(instance.nastavak_ij)
