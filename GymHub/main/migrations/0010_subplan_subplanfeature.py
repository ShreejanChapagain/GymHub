# Generated by Django 5.0.2 on 2024-02-15 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_gallery_galleryimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('price', models.IntegerField()),
                ('max_member', models.IntegerField(null=True)),
                ('highlight_status', models.BooleanField(default=False, null=True)),
                ('validity_days', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubPlanFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('subplan', models.ManyToManyField(to='main.subplan')),
            ],
        ),
    ]
