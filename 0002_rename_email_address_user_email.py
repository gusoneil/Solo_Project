# Generated by Django 3.2.4 on 2021-06-15 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviewapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email_address',
            new_name='email',
        ),
    ]
