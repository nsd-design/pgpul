# Generated by Django 4.2.6 on 2023-12-21 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='is_active',
        ),
    ]
