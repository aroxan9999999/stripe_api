# Generated by Django 4.1.1 on 2023-02-21 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stripe_api', '0004_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='many',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]