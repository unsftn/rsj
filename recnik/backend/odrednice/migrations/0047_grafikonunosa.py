# Generated by Django 3.2 on 2021-07-15 14:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('odrednice', '0046_varijantaodrednice_rod'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrafikonUnosa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip', models.IntegerField(choices=[(1, 'недељни принос'), (2, 'месечни принос'), (3, 'годишњи принос'), (4, 'недељни кумулативно'), (5, 'месечни кумулативно'), (6, 'годишњи кумулативно')], verbose_name='тип графикона')),
                ('vreme', models.DateTimeField(default=django.utils.timezone.now, verbose_name='време генерисања')),
                ('data', models.TextField(verbose_name='подаци')),
            ],
            options={
                'verbose_name': 'графикон уноса',
                'verbose_name_plural': 'графикони уноса',
            },
        ),
    ]
