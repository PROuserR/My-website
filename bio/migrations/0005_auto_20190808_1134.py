# Generated by Django 2.2.4 on 2019-08-08 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bio', '0004_auto_20190808_1107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='text',
            new_name='title',
        ),
    ]
