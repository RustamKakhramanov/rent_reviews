# Generated by Django 4.2.7 on 2023-12-29 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_searchtelegramuser_auth_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='search_accounts',
            field=models.ManyToManyField(blank=True, null=True, to='core.searchtelegramuser'),
        ),
    ]
