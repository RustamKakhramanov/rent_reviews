# Generated by Django 4.2.7 on 2023-12-20 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_search_entity_search_id_alter_search_leads_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchtelegramuser',
            name='auth_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
