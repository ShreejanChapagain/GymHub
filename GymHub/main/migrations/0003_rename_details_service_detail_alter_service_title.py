# Generated by Django 5.0.2 on 2024-02-13 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_banner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='details',
            new_name='detail',
        ),
        migrations.AlterField(
            model_name='service',
            name='title',
            field=models.CharField(max_length=150),
        ),
    ]
