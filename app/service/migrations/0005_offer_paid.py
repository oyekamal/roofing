# Generated by Django 4.2.1 on 2023-07-06 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_alter_offer_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]