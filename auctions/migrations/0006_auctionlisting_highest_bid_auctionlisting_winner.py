# Generated by Django 5.1.2 on 2024-10-21 17:14

import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_auctionlisting_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='highest_bid',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='won_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
