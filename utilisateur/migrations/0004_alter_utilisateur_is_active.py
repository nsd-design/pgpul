# Generated by Django 4.2.6 on 2023-12-21 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0003_utilisateur_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
