from django.apps import apps
from django.contrib import admin
from django.contrib.auth.models import Group

# Recuperer toutes les applications intallee

app_list = apps.get_app_configs()

# Supprime l'enregistrement du modèle Group existant
admin.site.unregister(Group)

for app in app_list:
    app_name = app.name.split('.')[-1]
    app_models = app.get_models()
    admin.site.register(app_models)
