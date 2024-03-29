# Generated by Django 4.0.3 on 2022-05-15 22:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reci', '0011_alter_pridev_lema'),
    ]

    operations = [
        migrations.CreateModel(
            name='Predlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tekst', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'предлог',
                'verbose_name_plural': 'предлози',
            },
        ),
        migrations.CreateModel(
            name='Recca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tekst', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'речца',
                'verbose_name_plural': 'речце',
            },
        ),
        migrations.CreateModel(
            name='Uzvik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tekst', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'узвик',
                'verbose_name_plural': 'узвици',
            },
        ),
        migrations.CreateModel(
            name='Veznik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tekst', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'везник',
                'verbose_name_plural': 'везници',
            },
        ),
        migrations.CreateModel(
            name='IzmenaVeznika',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operacija_izmene', models.PositiveSmallIntegerField(choices=[(1, 'креирана реч'), (2, 'измењена реч')], verbose_name='операција измене')),
                ('vreme', models.DateTimeField(default=django.utils.timezone.now, verbose_name='време')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='reci.userproxy', verbose_name='корисник')),
                ('veznik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reci.veznik', verbose_name='')),
            ],
            options={
                'verbose_name': 'измена везника',
                'verbose_name_plural': 'измене везника',
            },
        ),
        migrations.CreateModel(
            name='IzmenaUzvika',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operacija_izmene', models.PositiveSmallIntegerField(choices=[(1, 'креирана реч'), (2, 'измењена реч')], verbose_name='операција измене')),
                ('vreme', models.DateTimeField(default=django.utils.timezone.now, verbose_name='време')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='reci.userproxy', verbose_name='корисник')),
                ('uzvik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reci.uzvik', verbose_name='')),
            ],
            options={
                'verbose_name': 'измена узвика',
                'verbose_name_plural': 'измене узвика',
            },
        ),
        migrations.CreateModel(
            name='IzmenaRecce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operacija_izmene', models.PositiveSmallIntegerField(choices=[(1, 'креирана реч'), (2, 'измењена реч')], verbose_name='операција измене')),
                ('vreme', models.DateTimeField(default=django.utils.timezone.now, verbose_name='време')),
                ('recca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reci.recca', verbose_name='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='reci.userproxy', verbose_name='корисник')),
            ],
            options={
                'verbose_name': 'измена речце',
                'verbose_name_plural': 'измене речци',
            },
        ),
        migrations.CreateModel(
            name='IzmenaPredloga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operacija_izmene', models.PositiveSmallIntegerField(choices=[(1, 'креирана реч'), (2, 'измењена реч')], verbose_name='операција измене')),
                ('vreme', models.DateTimeField(default=django.utils.timezone.now, verbose_name='време')),
                ('predlog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reci.predlog', verbose_name='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='reci.userproxy', verbose_name='корисник')),
            ],
            options={
                'verbose_name': 'измена предлога',
                'verbose_name_plural': 'измене предлога',
            },
        ),
    ]
