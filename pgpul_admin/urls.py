from django.urls import path

from pgpul_admin.views import *

urlpatterns = [
    path("departement/", departement, name="departement"),
    path("departement/fac/", create_faculte, name="fac"),
    path("departement/dept/", create_department, name="dept"),
    path("departement/classe/", create_classe, name="classe"),
    path("matiere/", create_matiere, name="matiere"),
    path("matiere/get_departement/", matiere_par_departement, name="matiere_par_dept"),
    path("matiere/attribution/", attribuer_matiere_a_pro, name="attribution"),
    path("enseignant/", enseignant, name="enseignant"),
    path("enseignant/liste/", liste_enseignants, name="list_enseignants"),
]
