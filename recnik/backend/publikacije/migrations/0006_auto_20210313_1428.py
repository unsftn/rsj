# Generated by Django 3.1.3 on 2021-03-13 13:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('publikacije', '0005_publikacija_skracenica'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publikacija',
            name='vreme_unosa',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='време уноса'),
        ),
    ]