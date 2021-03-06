# Generated by Django 3.0.5 on 2020-05-10 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0024_auto_20200412_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopReview',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('review', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('rating', models.IntegerField(default=1)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.ShopReview')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
