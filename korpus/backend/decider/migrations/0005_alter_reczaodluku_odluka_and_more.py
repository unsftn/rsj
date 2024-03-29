# Generated by Django 4.1 on 2023-01-24 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decider', '0004_alter_reczaodluku_beleska'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reczaodluku',
            name='odluka',
            field=models.IntegerField(choices=[(1, 'без одлуке'), (2, 'иде у речник'), (3, 'не иде у речник'), (4, 'иде у проширени речник'), (5, 'уклонити из речника')], verbose_name='одлука'),
        ),
        migrations.AddIndex(
            model_name='reczaodluku',
            index=models.Index(fields=['broj_pojavljivanja'], name='decider_rec_broj_po_5e1a5b_idx'),
        ),
    ]
