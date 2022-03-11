import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import FajlPublikacije, Publikacija
from .utils import renumber_files


@receiver(post_delete, sender=FajlPublikacije)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.uploaded_file:
        if os.path.isfile(instance.uploaded_file.path):
            os.remove(instance.uploaded_file.path)
    renumber_files(instance.publikacija_id)


@receiver(pre_save, sender=FajlPublikacije)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = FajlPublikacije.objects.get(pk=instance.pk).uploaded_file
    except FajlPublikacije.DoesNotExist:
        return False
    new_file = instance.uploaded_file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
