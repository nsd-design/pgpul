# Generated by Django 4.2.6 on 2023-10-22 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0002_alter_utilisateur_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
