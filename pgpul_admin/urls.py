from django.urls import path

from pgpul_admin.views import departement, create_faculte

urlpatterns = [
    path("departement/", departement, name="departement"),
    path("departement/fac/", create_faculte, name="fac"),
]
