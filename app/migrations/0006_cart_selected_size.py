# Generated by Django 4.2.4 on 2024-04-29 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_cart_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='selected_size',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
