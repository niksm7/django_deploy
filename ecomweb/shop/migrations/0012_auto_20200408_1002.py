# Generated by Django 3.0.4 on 2020-04-08 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20200408_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderupdate',
            name='timestamp',
            field=models.DateField(auto_now_add=True),
        ),
    ]