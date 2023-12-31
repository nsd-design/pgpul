# Generated by Django 4.2.6 on 2023-11-05 21:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pgpul_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classe',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classe',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classe_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='classe',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='classe',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classe_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
