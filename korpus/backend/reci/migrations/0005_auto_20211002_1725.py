# Generated by Django 3.2.7 on 2021-10-02 15:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reci', '0004_auto_20210927_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Glagol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gl_rod', models.IntegerField(blank=True, choices=[(1, 'прелазни'), (2, 'непрелазни'), (3, 'повратни'), (4, 'прелазни и непрелазни'), (5, 'непрелазни и прелазни'), (6, 'прелазни (непрелазни)'), (7, 'непрелазни (прелазни)')], null=True, verbose_name='глаголски род')),
                ('gl_vid', models.IntegerField(blank=True, choices=[(1, 'свршени'), (2, 'несвршени'), (3, 'свршени и несвршени'), (4, 'несвршени и свршени'), (5, 'свршени (несвршени)'), (6, 'несвршени (свршени)')], null=True, verbose_name='глаголски вид')),
                ('infinitiv', models.CharField(blank=True, max_length=50, null=True, verbose_name='инфинитив')),
                ('recnik_id', models.IntegerField(blank=True, null=True, verbose_name='ID одреднице у речнику')),
                ('vreme_kreiranja', models.DateTimeField(default=django.utils.timezone.now, verbose_name='време креирања')),
                ('poslednja_izmena', models.DateTimeField(default=django.utils.timezone.now, verbose_name='време последње измене')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='reci.statusreci', verbose_name='статус речи')),
            ],
            options={
                'verbose_name': 'глагол',
                'verbose_name_plural': 'глаголи',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='OblikGlagola',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vreme', models.IntegerField(choices=[(1, 'презент'), (2, 'футур 1'), (1, 'аорист'), (1, 'имперфекат'), (1, 'императив')], verbose_name='време')),
                ('jd1', models.CharField(blank=True, max_length=50, null=True, verbose_name='прво лице једнине')),
                ('jd2', models.CharField(blank=True, max_length=50, null=True, verbose_name='друго лице једнине')),
                ('jd3', models.CharField(blank=True, max_length=50, null=True, verbose_name='треће лице једнине')),
                ('mn1', models.CharField(blank=True, max_length=50, null=True, verbose_name='прво лице множине')),
                ('mn2', models.CharField(blank=True, max_length=50, null=True, verbose_name='друго лице множине')),
                ('mn3', models.CharField(blank=True, max_length=50, null=True, verbose_name='треће лице множине')),
                ('glagol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reci.glagol', verbose_name='глагол')),
            ],
            options={
                'verbose_name': 'глаголски облик',
                'verbose_name_plural': 'глаголски облици',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='VarijanteGlagola',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('varijanta', models.IntegerField(choices=[(1, 'пр.л.јед.'), (2, 'др.л.јед.'), (3, 'тр.л.јед.'), (4, 'пр.л.мн.'), (5, 'др.л.мн.'), (6, 'тр.л.мн.')], verbose_name='варијанта')),
                ('tekst', models.CharField(blank=True, max_length=50, null=True, verbose_name='текст')),
                ('oblik_glagola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reci.oblikglagola', verbose_name='облик глагола')),
            ],
            options={
                'verbose_name': 'варијанта глагола',
                'verbose_name_plural': 'варијанте глагола',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='IzmenaGlagola',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operacija_izmene', models.PositiveSmallIntegerField(choices=[(1, 'креирана реч'), (2, 'измењена реч')], verbose_name='операција измене')),
                ('vreme', models.DateTimeField(default=django.utils.timezone.now, verbose_name='време')),
                ('glagol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reci.glagol', verbose_name='глагол')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='reci.userproxy', verbose_name='корисник')),
            ],
            options={
                'verbose_name': 'измена глагола',
                'verbose_name_plural': 'измене глагола',
            },
        ),
        migrations.AddIndex(
            model_name='oblikglagola',
            index=models.Index(fields=['jd1'], name='reci_oblikg_jd1_b4215f_idx'),
        ),
        migrations.AddIndex(
            model_name='glagol',
            index=models.Index(fields=['infinitiv'], name='reci_glagol_infinit_f425e9_idx'),
        ),
    ]
