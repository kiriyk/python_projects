# Generated by Django 4.1.3 on 2022-11-28 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0009_alter_news_options_news_tag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'permissions': (('publish_news', 'Can publish'),), 'verbose_name_plural': 'News'},
        ),
    ]
