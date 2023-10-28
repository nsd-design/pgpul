from django.urls import path

from pgpul_admin.views import *

urlpatterns = [
    path("departement/", departement, name="departement"),
    path("departement/fac/", create_faculte, name="fac"),
    path("departement/dept/", create_department, name="dept"),
    path("departement/classe/", create_classe, name="classe"),
]
