# Generated by Django 2.2 on 2022-11-18 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0007_auto_20221118_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='username',
            field=models.CharField(blank=True, max_length=30, verbose_name='Username'),
        ),
    ]
