# Generated by Django 3.2.4 on 2021-06-16 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewapp', '0003_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='year_released',
            field=models.CharField(max_length=255),
        ),
    ]