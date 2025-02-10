# Generated by Django 4.2 on 2023-05-14 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=30)),
                ('emails', models.EmailField(max_length=254)),
                ('msg', models.CharField(max_length=3000)),
            ],
        ),
        migrations.DeleteModel(
            name='message',
        ),
    ]
