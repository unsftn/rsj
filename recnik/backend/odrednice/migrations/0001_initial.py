# Generated by Django 3.1.3 on 2020-12-20 13:31

import concurrency.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kolokacija',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('napomena', models.CharField(max_length=2000, verbose_name='напомена')),
            ],
            options={
                'verbose_name': 'колокација',
                'verbose_name_plural': 'колокације',
            },
        ),
        migrations.CreateModel(
            name='Kvalifikator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.CharField(max_length=50, verbose_name='назив')),
            ],
            options={
                'verbose_name': 'квалификатор',
                'verbose_name_plural': 'квалификатори',
            },
        ),
        migrations.CreateModel(
            name='Odrednica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rec', models.CharField(blank=True, max_length=50, null=True, verbose_name='реч')),
                ('vrsta', models.IntegerField(choices=[(0, 'именица'), (1, 'глагол'), (2, 'придев'), (3, 'прилог'), (4, 'предлог'), (5, 'заменица'), (6, 'узвик'), (7, 'речца'), (8, 'везник'), (9, 'број')], verbose_name='врста')),
                ('rod', models.IntegerField(choices=[(1, 'мушки'), (2, 'женски'), (3, 'средњи')], default=0, verbose_name='род')),
                ('nastavak', models.CharField(blank=True, max_length=50, null=True, verbose_name='наставак')),
                ('info', models.CharField(blank=True, max_length=2000, null=True, verbose_name='инфо')),
                ('glagolski_vid', models.IntegerField(choices=[(0, 'непознат'), (1, 'свршени'), (2, 'несвршени'), (3, 'двовидски')], verbose_name='глаголски вид')),
                ('glagolski_rod', models.IntegerField(choices=[(0, 'непознат'), (1, 'прелазни'), (2, 'непрелазни'), (3, 'повратни'), (4, 'узајамно повратни')], verbose_name='глаголски род')),
                ('prezent', models.CharField(blank=True, max_length=50, null=True, verbose_name='презент')),
                ('broj_pregleda', models.IntegerField(default=0, verbose_name='број прегледа')),
                ('vreme_kreiranja', models.DateTimeField(default=django.utils.timezone.now, verbose_name='време креирања')),
                ('poslednja_izmena', models.DateTimeField(default=django.utils.timezone.now, verbose_name='време последње измене')),
                ('stanje', models.IntegerField(verbose_name='стање')),
                ('version', concurrency.fields.AutoIncVersionField(default=0, help_text='record revision number')),
            ],
            options={
                'verbose_name': 'одредница',
                'verbose_name_plural': 'одреднице',
            },
        ),
        migrations.CreateModel(
            name='OperacijaIzmene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.CharField(max_length=50, verbose_name='назив')),
            ],
            options={
                'verbose_name': 'операција измене одреднице',
                'verbose_name_plural': 'операције измена одредница',
            },
        ),
        migrations.CreateModel(
            name='Znacenje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tekst', models.CharField(max_length=2000, verbose_name='текст')),
                ('odrednica_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='odrednice.odrednica', verbose_name='одредница')),
            ],
            options={
                'verbose_name': 'значење',
                'verbose_name_plural': 'значења',
            },
        ),
        migrations.CreateModel(
            name='Sinonim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redni_broj', models.PositiveSmallIntegerField(verbose_name='редни број')),
                ('ima_sinonim_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ima_sinonim', to='odrednice.odrednica', verbose_name='одредница има синоним')),
                ('u_vezi_sa_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sinonim_u_vezi_sa', to='odrednice.odrednica', verbose_name='у вези са одредницом')),
            ],
            options={
                'verbose_name': 'синоним',
                'verbose_name_plural': 'синоними',
            },
        ),
        migrations.CreateModel(
            name='RecUKolokaciji',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redni_broj', models.PositiveSmallIntegerField(verbose_name='редни број')),
                ('kolokacija_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='odrednice.kolokacija', verbose_name='колокација')),
                ('odrednica_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='odrednice.odrednica', verbose_name='одредница')),
            ],
            options={
                'verbose_name': 'реч у колокацији',
                'verbose_name_plural': 'речи у колокацији',
            },
        ),
        migrations.CreateModel(
            name='Podznacenje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tekst', models.CharField(max_length=2000, verbose_name='текст')),
                ('znacenje_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='odrednice.znacenje', verbose_name='значење')),
            ],
            options={
                'verbose_name': 'подзначење',
                'verbose_name_plural': 'подзначења',
            },
        ),
        migrations.CreateModel(
            name='KvalifikatorOdrednice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redni_broj', models.PositiveSmallIntegerField(verbose_name='редни број')),
                ('kvalifikator_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='odrednice.kvalifikator', verbose_name='квалификатор')),
                ('odrednica_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='odrednice.odrednica', verbose_name='одредница')),
            ],
            options={
                'verbose_name': 'квалификатор одреднице',
                'verbose_name_plural': 'квалификатори одредница',
            },
        ),
        migrations.AddField(
            model_name='kolokacija',
            name='odrednica_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='odrednice.odrednica', verbose_name='одредница'),
        ),
        migrations.CreateModel(
            name='IzrazFraza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opis', models.CharField(max_length=2000, verbose_name='опис')),
                ('pripada_odrednici_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pripada_odrednici', to='odrednice.odrednica', verbose_name='одредница')),
                ('u_vezi_sa_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='izrazfraza_u_vezi_sa', to='odrednice.odrednica', verbose_name='у вези са одредницом')),
            ],
            options={
                'verbose_name': 'израз фраза',
                'verbose_name_plural': 'изрази фразе',
            },
        ),
        migrations.CreateModel(
            name='IzmenaOdrednice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vreme', models.DateTimeField(default=django.utils.timezone.now, verbose_name='време')),
                ('odrednica_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='odrednice.odrednica', verbose_name='одредница')),
                ('operacija_izmene_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='odrednice.operacijaizmene', verbose_name='операција измене одреднице')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='корисник')),
            ],
            options={
                'verbose_name': 'измена одреднице',
                'verbose_name_plural': 'измене одредница',
            },
        ),
        migrations.CreateModel(
            name='Antonim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redni_broj', models.PositiveSmallIntegerField(verbose_name='редни број')),
                ('ima_antonim_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ima_antonim', to='odrednice.odrednica', verbose_name='одредница има антоним')),
                ('u_vezi_sa_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='antonim_u_vezi_sa', to='odrednice.odrednica', verbose_name='у вези са одредницом')),
            ],
            options={
                'verbose_name': 'антоним',
                'verbose_name_plural': 'антоними',
            },
        ),
    ]
