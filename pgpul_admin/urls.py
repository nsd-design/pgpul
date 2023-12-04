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
    path("matiere/table_matiere/<int:id_matiere>", afficher_table_matieres, name="table_matiere"),
    path("enseignant/", enseignant, name="enseignant"),
    path("enseignant/liste/", liste_enseignants, name="list_enseignants"),
    path("etudiant/", create_etudiant, name="etudiant"),
    path("etudiant/liste/", liste_etudiants, name="liste_etudiant"),
    path("cours/", cours, name="cours"),
    path("cours/liste/", liste_des_matieres, name="liste_matieres"),
    path("cours/sommaire/<int:id_matiere>", sommaire_par_matiere, name="sommaire_par_matiere"),
    path("cours/lire_cours/<int:id_cours>/<int:id_matiere>/", affiche_contenu_cours, name="lire_cours"),
    path("sommaire/", create_sommaire, name="sommaire"),
]
