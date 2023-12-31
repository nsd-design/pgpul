# Generated by Django 4.2.6 on 2023-12-21 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0002_remove_utilisateur_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
