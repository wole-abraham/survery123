# Generated by Django 5.1.4 on 2025-01-25 12:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities_report', '0002_remove_activities_global_id_activities_chainage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='date_of_activity',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 25, 4, 22, 49, 278793)),
        ),
    ]
