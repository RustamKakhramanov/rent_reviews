# Generated by Django 4.2.7 on 2023-11-19 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_telegramuser_is_accepted_rules'),
    ]

    operations = [
        migrations.RenameField(
            model_name='telegramuser',
            old_name='expire_at',
            new_name='expired_at',
        ),
    ]