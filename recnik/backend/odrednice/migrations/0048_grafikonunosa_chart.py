# Generated by Django 3.2 on 2021-07-15 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odrednice', '0047_grafikonunosa'),
    ]

    operations = [
        migrations.AddField(
            model_name='grafikonunosa',
            name='chart',
            field=models.TextField(default=None, verbose_name='графикон'),
            preserve_default=False,
        ),
    ]
