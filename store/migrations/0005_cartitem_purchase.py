# Generated by Django 5.1 on 2024-11-01 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_merge_0002_customer_address_0003_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='purchase',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
