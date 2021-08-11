from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Kvalifikator, Odrednica
from .text import remove_punctuation


@receiver(post_save, sender=Kvalifikator)
def sync_kvalifikator_to_memory(sender, instance, created, raw, using, update_fields, **kwargs):
    if created and using == 'default':
        instance.save(using='memory')


@receiver(pre_save, sender=Odrednica)
def create_sortable_rec(sender, instance, raw, using, update_fields, **kwargs):
    instance.sortable_rec = remove_punctuation(instance.rec)
