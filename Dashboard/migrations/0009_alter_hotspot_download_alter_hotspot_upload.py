# Generated by Django 4.0.3 on 2022-04-22 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0008_apprenticeshipregistration_averagetestscores_and_more'),
    ]

    operations = [
  


            migrations.CreateModel(
            name='hotspot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('download',models.FloatField(db_column='Download', max_length=100, blank=True, null=True)),
                ('upload', models.FloatField(db_column='Upload', max_length=20, blank=True, null=True)),
                ('name', models.CharField(db_column='Name', max_length=20, blank=True, null=True)),
                ('address', models.CharField(db_column='Address', max_length=20, blank=True, null=True)),
            ],
            options={
                'db_table': 'hotspot',
            },
        ),

    ]
