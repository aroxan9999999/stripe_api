# Generated by Django 4.1.1 on 2023-02-21 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_api', '0006_order_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='item',
        ),
        migrations.AddField(
            model_name='order',
            name='item_pk',
            field=models.IntegerField(default=0),
        ),
    ]