# Generated by Django 4.1 on 2022-12-20 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decider', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reczaodluku',
            name='beleska',
            field=models.TextField(blank=True, max_length=500, verbose_name='белешка'),
        ),
    ]
