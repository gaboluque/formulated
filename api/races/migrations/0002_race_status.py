# Generated by Django 4.2.21 on 2025-06-21 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='status',
            field=models.CharField(choices=[('scheduled', 'Scheduled'), ('ongoing', 'Ongoing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled', max_length=255),
        ),
    ]
