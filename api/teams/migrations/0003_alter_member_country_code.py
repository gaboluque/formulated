# Generated by Django 4.2.21 on 2025-06-24 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_member_country_code_member_driver_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='country_code',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
