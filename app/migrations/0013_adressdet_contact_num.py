# Generated by Django 4.2.4 on 2024-05-07 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_adressdet_contact_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='adressdet',
            name='contact_num',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
