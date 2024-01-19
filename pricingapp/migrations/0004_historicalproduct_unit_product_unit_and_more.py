# Generated by Django 5.0.1 on 2024-01-18 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricingapp', '0003_historicalproduct_weight_product_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproduct',
            name='unit',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Foreign key of Product', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='pricingapp.productunit'),
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(help_text='Foreign key of Product', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quote_items', to='pricingapp.productunit'),
        ),
        migrations.DeleteModel(
            name='UnitConversion',
        ),
    ]
