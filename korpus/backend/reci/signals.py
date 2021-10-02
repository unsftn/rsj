from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Imenica, Glagol
from .indexer import save_imenica, save_glagol


@receiver(post_save, sender=Imenica)
def index_imenica(sender, instance, created, raw, using, update_fields, **kwargs):
    save_imenica(instance)


@receiver(post_save, sender=Glagol)
def index_glagol(sender, instance, created, raw, using, update_fields, **kwargs):
    save_glagol(instance)
