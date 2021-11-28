# Generated by Django 3.2.9 on 2021-11-15 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0004_productsinfo_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsinfo',
            name='primary_essential',
            field=models.CharField(blank=True, db_column='Primary_Essential_Function', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='productsinfo',
            name='product_name',
            field=models.CharField(blank=True, db_column='Product_Name', max_length=255, null=True),
        ),
    ]
