# Generated by Django 3.1.3 on 2020-12-07 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publikacije', '0002_auto_20201205_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='publikacija',
            name='potkorpus',
            field=models.IntegerField(choices=[(0, 'непознат'), (1, 'новински'), (2, 'разговорни')], default=0, verbose_name='поткорпус'),
        ),
    ]
