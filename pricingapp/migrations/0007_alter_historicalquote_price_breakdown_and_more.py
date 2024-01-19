# Generated by Django 5.0.1 on 2024-01-18 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricingapp', '0006_historicalquote_quote_historicalquoteitem_quoteitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalquote',
            name='price_breakdown',
            field=models.JSONField(default=dict, help_text='Breakdown of the total price'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='price_breakdown',
            field=models.JSONField(default=dict, help_text='Breakdown of the total price'),
        ),
    ]
