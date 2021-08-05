import unicodedata
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Kvalifikator, Odrednica


def remove_punctuation(text):
    cleared_text = ''.join(c for c in text if unicodedata.category(c) in ['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'NI'])
    return cleared_text


@receiver(post_save, sender=Kvalifikator)
def sync_kvalifikator_to_memory(sender, instance, created, raw, using, update_fields, **kwargs):
    if created and using == 'default':
        instance.save(using='memory')


@receiver(pre_save, sender=Odrednica)
def create_sortable_rec(sender, instance, raw, using, update_fields, **kwargs):
    instance.sortable_rec = remove_punctuation(instance.rec)
