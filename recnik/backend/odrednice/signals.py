from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Kvalifikator


@receiver(pre_save, sender=Kvalifikator)
def sync_kvalifikator_to_memory(sender, instance, raw, using, update_fields, **kwargs):
    if using == 'default':
        instance.save(using='memory')
