# Generated by Django 4.2.7 on 2023-11-29 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_search_delete_searchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='telegram_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
