# Generated by Django 4.2.1 on 2023-06-20 05:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_testimonials'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonials',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
