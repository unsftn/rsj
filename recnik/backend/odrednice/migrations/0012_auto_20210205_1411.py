# Generated by Django 3.1.3 on 2021-02-05 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('odrednice', '0011_auto_20210205_1410'),
    ]

    operations = [
        migrations.RenameField(
            model_name='antonim',
            old_name='ima_antonim_id',
            new_name='ima_antonim',
        ),
        migrations.RenameField(
            model_name='antonim',
            old_name='u_vezi_sa_id',
            new_name='u_vezi_sa',
        ),
    ]
