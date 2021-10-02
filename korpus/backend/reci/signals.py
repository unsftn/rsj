from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Imenica, Glagol, Pridev
from .indexer import index_imenica, index_glagol, index_pridev


@receiver(post_save, sender=Imenica)
def reindex_imenica(sender, instance, created, raw, using, update_fields, **kwargs):
    index_imenica(instance)


@receiver(post_save, sender=Glagol)
def reindex_glagol(sender, instance, created, raw, using, update_fields, **kwargs):
    index_glagol(instance)


@receiver(post_save, sender=Pridev)
def reindex_pridev(sender, instance, created, raw, using, update_fields, **kwargs):
    index_pridev(instance)
