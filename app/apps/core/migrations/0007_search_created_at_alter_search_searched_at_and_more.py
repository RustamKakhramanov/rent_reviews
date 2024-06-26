# Generated by Django 4.2.7 on 2023-12-04 14:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_telegramuser_telegram_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='search',
            name='searched_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='search',
            name='status',
            field=models.CharField(choices=[('initial', 'В сбооре'), ('ready', 'Ожидает поиска'), ('in_process', 'В процессе'), ('error', 'Ошибка'), ('finished', 'Завершен')], default='initial', max_length=50),
        ),
        migrations.AlterField(
            model_name='search',
            name='table_link',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
