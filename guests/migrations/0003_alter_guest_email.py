# Generated by Django 5.1.3 on 2024-11-26 07:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("guests", "0002_rename_plus_ones_guest_number_of_companions_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="guest",
            name="email",
            field=models.EmailField(max_length=255),
        ),
    ]
