# Generated by Django 5.0.9 on 2025-04-09 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_alter_order_created_timestamp"),
    ]

    operations = [
        migrations.DeleteModel(
            name="OrderItem",
        ),
    ]
