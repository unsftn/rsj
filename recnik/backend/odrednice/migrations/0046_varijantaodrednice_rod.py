# Generated by Django 3.2 on 2021-07-13 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odrednice', '0045_konkordansa_izraz_fraza'),
    ]

    operations = [
        migrations.AddField(
            model_name='varijantaodrednice',
            name='rod',
            field=models.IntegerField(blank=True, choices=[(1, 'мушки'), (2, 'женски'), (3, 'средњи'), (4, 'мушки (женски)'), (5, 'женски (мушки)'), (6, 'мушки (средњи)'), (7, 'средњи (мушки)'), (8, 'женски (средњи)'), (9, 'средњи (женски)')], default=0, null=True, verbose_name='род'),
        ),
    ]