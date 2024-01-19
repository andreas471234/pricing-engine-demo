# Generated by Django 5.0.1 on 2024-01-17 14:43

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(db_index=True, help_text='Customer unique code', max_length=127, unique=True)),
                ('name', models.CharField(help_text='Name of the customer', max_length=127)),
                ('address', models.TextField(help_text='Address of Customer')),
                ('city', models.CharField(help_text='City of Customer address', max_length=127)),
                ('state', models.CharField(help_text='State of Customer address', max_length=127)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(db_index=True, help_text='Product unique code', max_length=127, unique=True)),
                ('name', models.CharField(help_text='Product name', max_length=127)),
                ('market_price', models.DecimalField(decimal_places=4, default=0.0, help_text='Market price per unit of product', max_digits=25)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(help_text='Product unit name', max_length=127)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(db_index=True, help_text='Supplier unique code', max_length=127, unique=True)),
                ('address', models.TextField(help_text='Address of Supplier')),
                ('city', models.CharField(help_text='City of Supplier address', max_length=127)),
                ('state', models.CharField(help_text='State of Supplier address', max_length=127)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalCustomer',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(db_index=True, help_text='Customer unique code', max_length=127)),
                ('name', models.CharField(help_text='Name of the customer', max_length=127)),
                ('address', models.TextField(help_text='Address of Customer')),
                ('city', models.CharField(help_text='City of Customer address', max_length=127)),
                ('state', models.CharField(help_text='State of Customer address', max_length=127)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical customer',
                'verbose_name_plural': 'historical customers',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(db_index=True, help_text='Product unique code', max_length=127)),
                ('name', models.CharField(help_text='Product name', max_length=127)),
                ('market_price', models.DecimalField(decimal_places=4, default=0.0, help_text='Market price per unit of product', max_digits=25)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical product',
                'verbose_name_plural': 'historical products',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalProductUnit',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(help_text='Product unit name', max_length=127)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical product unit',
                'verbose_name_plural': 'historical product units',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSupplier',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(db_index=True, help_text='Supplier unique code', max_length=127)),
                ('address', models.TextField(help_text='Address of Supplier')),
                ('city', models.CharField(help_text='City of Supplier address', max_length=127)),
                ('state', models.CharField(help_text='State of Supplier address', max_length=127)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical supplier',
                'verbose_name_plural': 'historical suppliers',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalFleet',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(db_index=True, help_text='Fleet unique code', max_length=127)),
                ('name', models.CharField(help_text='Fleet name', max_length=127)),
                ('capacity', models.FloatField(default=0, help_text='Fleet max capacity')),
                ('cost', models.JSONField(help_text='Fleet cost')),
                ('type', models.CharField(help_text='Fleet type', max_length=127)),
                ('pool', models.CharField(help_text='Fleet pool to calculate the shipping cost', max_length=127)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('unit', models.ForeignKey(blank=True, db_constraint=False, help_text='Foreign key of capacity unit', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='pricingapp.productunit')),
            ],
            options={
                'verbose_name': 'historical fleet',
                'verbose_name_plural': 'historical fleets',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Fleet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(db_index=True, help_text='Fleet unique code', max_length=127, unique=True)),
                ('name', models.CharField(help_text='Fleet name', max_length=127)),
                ('capacity', models.FloatField(default=0, help_text='Fleet max capacity')),
                ('cost', models.JSONField(help_text='Fleet cost')),
                ('type', models.CharField(help_text='Fleet type', max_length=127)),
                ('pool', models.CharField(help_text='Fleet pool to calculate the shipping cost', max_length=127)),
                ('unit', models.ForeignKey(help_text='Foreign key of capacity unit', on_delete=django.db.models.deletion.CASCADE, related_name='fleets', to='pricingapp.productunit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SupplierProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('stock', models.FloatField(default=0, help_text='Stock of product sell by supplier')),
                ('product', models.ForeignKey(help_text='Foreign key of Product', on_delete=django.db.models.deletion.CASCADE, related_name='supplier_maps', to='pricingapp.product')),
                ('supplier', models.ForeignKey(help_text='Foreign key of Supplier', on_delete=django.db.models.deletion.CASCADE, related_name='product_maps', to='pricingapp.supplier')),
                ('unit', models.ForeignKey(help_text='Foreign key of unit for the default stock', on_delete=django.db.models.deletion.CASCADE, to='pricingapp.productunit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('price_per_unit', models.DecimalField(decimal_places=4, default=0.0, help_text='Price per unit of product', max_digits=25)),
                ('min_qty', models.FloatField(default=0, help_text='Minimal qty that they sell this unit in to get these prices')),
                ('unit', models.ForeignKey(help_text='Foreign key of unit', on_delete=django.db.models.deletion.CASCADE, to='pricingapp.productunit')),
                ('supplier_map', models.ForeignKey(help_text='Foreign key of supplier product map', on_delete=django.db.models.deletion.CASCADE, related_name='price_maps', to='pricingapp.supplierproduct')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UnitConversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('conversion_rate', models.FloatField(default=1, help_text='Conversion rate of the unit')),
                ('unit_from', models.ForeignKey(help_text='Foreign key of Unit', on_delete=django.db.models.deletion.CASCADE, related_name='from_unit', to='pricingapp.productunit')),
                ('unit_to', models.ForeignKey(help_text='Foreign key of Unit', on_delete=django.db.models.deletion.CASCADE, related_name='to_unit', to='pricingapp.productunit')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
