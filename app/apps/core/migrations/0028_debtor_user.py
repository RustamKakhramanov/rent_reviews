# Generated by Django 4.2.5 on 2024-03-25 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0027_alter_debtor_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="debtor",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.telegramuser",
            ),
        ),
    ]
