# Generated by Django 4.1.3 on 2022-11-30 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_code', models.CharField(max_length=20, verbose_name='Vendor code')),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('price', models.IntegerField(verbose_name='Price')),
            ],
        ),
    ]
