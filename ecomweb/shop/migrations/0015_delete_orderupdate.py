# Generated by Django 3.0.4 on 2020-04-08 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_remove_orderupdate_timestamp1'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderUpdate',
        ),
    ]
