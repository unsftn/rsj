# Generated by Django 3.2 on 2021-08-05 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odrednice', '0048_grafikonunosa_chart'),
    ]

    operations = [
        migrations.AddField(
            model_name='odrednica',
            name='sortable_rec',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='реч за сортирање'),
        ),
    ]