# Generated by Django 4.2.4 on 2024-05-14 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
