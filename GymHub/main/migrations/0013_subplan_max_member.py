# Generated by Django 5.0.2 on 2024-02-29 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_subplan_highlight_status_alter_subplan_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='subplan',
            name='max_member',
            field=models.IntegerField(null=True),
        ),
    ]
