# Generated by Django 2.2 on 2019-11-05 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='StockControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_quantity', models.IntegerField()),
                ('total_value', models.IntegerField()),
                ('item_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Item')),
                ('stock_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Category')),
                ('stock_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Location')),
            ],
        ),
    ]
