# Generated by Django 3.0.4 on 2020-04-10 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200410_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='thumbnail',
            field=models.ImageField(default='', upload_to='blog/images'),
        ),
    ]