# Generated by Django 4.2 on 2023-05-03 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voyage',
            name='pays',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
