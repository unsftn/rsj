# Generated by Django 3.2 on 2021-08-16 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odrednice', '0053_auto_20210816_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='odrednica',
            name='glagolski_rod',
            field=models.IntegerField(blank=True, choices=[(1, 'прелазни'), (2, 'непрелазни'), (3, 'повратни'), (4, 'прелазни и непрелазни'), (5, 'непрелазни и прелазни'), (6, 'прелазни (непрелазни)'), (7, 'непрелазни (прелазни)'), (8, '(се) облик')], null=True, verbose_name='глаголски род'),
        ),
    ]