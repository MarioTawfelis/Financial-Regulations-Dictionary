# Generated by Django 2.0 on 2019-01-19 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190119_2131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='location',
            new_name='company',
        ),
    ]
