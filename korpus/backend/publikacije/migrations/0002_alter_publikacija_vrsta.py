# Generated by Django 3.2.7 on 2021-10-07 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publikacije', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publikacija',
            name='vrsta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='publikacije.vrstapublikacije', verbose_name='врста'),
        ),
    ]