# Generated by Django 3.2.13 on 2022-05-22 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Test', '0006_auto_20220522_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relate',
            name='relation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test', to='Test.testapp'),
        ),
    ]
