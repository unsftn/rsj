# Generated by Django 3.2 on 2021-04-21 18:24

from django.db import migrations
import django.db.models.functions.comparison


class Migration(migrations.Migration):

    dependencies = [
        ('odrednice', '0029_auto_20210421_1950'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kvalifikator',
            options={'ordering': [django.db.models.functions.comparison.Collate('skracenica', 'utf8mb4_unicode_ci')], 'verbose_name': 'квалификатор', 'verbose_name_plural': 'квалификатори'},
        ),
    ]