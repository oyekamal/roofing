# Generated by Django 4.2.1 on 2023-05-28 06:09

from django.db import migrations
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_serviceprovider_address_serviceprovider_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceprovider',
            name='location',
            field=location_field.models.plain.PlainLocationField(default=1, max_length=63),
            preserve_default=False,
        ),
    ]
