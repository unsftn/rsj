# Generated by Django 3.1.3 on 2021-03-13 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publikacije', '0004_publikacija_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='publikacija',
            name='skracenica',
            field=models.CharField(default='-', max_length=100, verbose_name='скраћеница'),
        ),
    ]
