# Generated by Django 2.2.4 on 2019-08-03 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.TextField()),
                ('content', models.TextField()),
                ('header', models.TextField()),
                ('meta', models.TextField()),
            ],
        ),
    ]
