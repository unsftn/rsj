# Generated by Django 3.1.3 on 2021-03-24 20:48

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('odrednice', '0027_auto_20210324_2142'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='izmenaodrednice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='odrednice.userproxy', verbose_name='корисник'),
        ),
        migrations.AlterField(
            model_name='odrednica',
            name='obradjivac',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='odrednice_obradjivaca', to='odrednice.userproxy', verbose_name='obradjivac'),
        ),
        migrations.AlterField(
            model_name='odrednica',
            name='redaktor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='odrednice_redaktora', to='odrednice.userproxy', verbose_name='obradjivac'),
        ),
        migrations.AlterField(
            model_name='odrednica',
            name='urednik',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='odrednice_urednika', to='odrednice.userproxy', verbose_name='obradjivac'),
        ),
    ]
