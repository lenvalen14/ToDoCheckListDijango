# Generated by Django 5.2.4 on 2025-07-17 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subtask",
            name="duration",
        ),
        migrations.RemoveField(
            model_name="subtask",
            name="start_day",
        ),
    ]
