# Generated by Django 2.2 on 2022-11-24 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0003_alter_profile_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_verified',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
