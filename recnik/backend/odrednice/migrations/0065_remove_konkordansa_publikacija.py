# Generated by Django 4.1.5 on 2023-02-18 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('odrednice', '0064_konkordansa_korpus_izvor_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='konkordansa',
            name='publikacija',
        ),
    ]