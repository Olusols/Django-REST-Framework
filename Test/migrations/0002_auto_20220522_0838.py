# Generated by Django 3.2.13 on 2022-05-22 07:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testapp',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='testapp',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='testapp',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
