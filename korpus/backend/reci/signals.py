from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Imenica, Glagol, Pridev
from functools import wraps


def skip_indexing():
    def _skip_indexing(signal_func):
        @wraps(signal_func)
        def _decorator(sender, instance, **kwargs):
            if hasattr(instance, 'skip_indexing'):
                return None
            return signal_func(sender, instance, **kwargs)
        return _decorator
    return _skip_indexing


# @receiver(post_save, sender=Imenica)
# @skip_indexing()
# def reindex_imenica(sender, instance, created, raw, using, update_fields, **kwargs):
#     index_imenica(instance)
#
#
# @receiver(post_save, sender=Glagol)
# @skip_indexing()
# def reindex_glagol(sender, instance, created, raw, using, update_fields, **kwargs):
#     index_glagol(instance)
#
#
# @receiver(post_save, sender=Pridev)
# @skip_indexing()
# def reindex_pridev(sender, instance, created, raw, using, update_fields, **kwargs):
#     index_pridev(instance)
