from django.db import models
from tinymce.models import HTMLField

# from django.conf import settings
from utilisateur.models import Utilisateur


class Faculte(models.Model):
    status = [
        (1, "Actif"),
        (2, "Supprimer")
    ]
    statut = models.SmallIntegerField(choices=status, default=1)
    nom_fac = models.CharField(max_length=50)
    code_fac = models.IntegerField(unique=True)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="faculte_created_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="faculte_updated_by")
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom_fac}"


class Departement(models.Model):
    status = [
        (1, "Actif"),
        (2, "Supprimer")
    ]
    statut = models.SmallIntegerField(choices=status, default=1)
    nom_dept = models.CharField(max_length=50)
    code_dept = models.IntegerField(unique=True)
    dept_fac = models.ForeignKey(Faculte, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="departement_created_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="departement_updated_by")
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom_dept} - {self.code_dept}"


class Enseignant(Utilisateur):
    gender = [
        (1, "Féminin"),
        (2, "Masculin"),
    ]
    status = [
        (1, "Actif"),
        (2, "Supprimer")
    ]
    statut = models.SmallIntegerField(choices=status, default=1)
    genre_ens = models.SmallIntegerField(choices=gender)
    tel_ens = models.CharField(max_length=12)
    specialite_ens = models.CharField(max_length=40)
    departement_principal = models.ForeignKey(Departement, on_delete=models.SET_NULL,
                                              related_name="departement_principal_enseignant", null=True)
    departements_enseigne = models.ManyToManyField(Departement, related_name="departements_enseigne_enseignant")
    adresse_en = models.CharField(max_length=30)
    photo_ens = models.ImageField(upload_to="images/", blank=True, null=True)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="enseignant_created_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="enseignant_updated_by")
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Etudiant(Utilisateur):
    gender = [
        (1, "Féminin"),
        (2, "Masculin"),
    ]
    matricule = models.CharField(max_length=15, unique=True)
    genre_etd = models.SmallIntegerField(choices=gender)
    tel_etd = models.CharField(max_length=12)
    departement_etd = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name="departement_de_etudiant")
    photo_ens = models.ImageField(upload_to="images/", blank=True, null=True)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name="etudiant_created_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   blank=True, related_name="etudiant_updated_by")
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.matricule}"


class Classe(models.Model):
    designation = models.CharField(max_length=40, unique=True)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="classe_created_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="classe_updated_by")
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.designation}"


class Matiere(models.Model):
    status = [
        (1, "Actif"),
        (2, "Supprimer")
    ]
    statut = models.SmallIntegerField(choices=status, default=1)
    nom_mat = models.CharField(max_length=40)
    classe_mat = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="classe_de_matiere")
    dept_mat = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name="departement_matiere")
    enseigne_par = models.ManyToManyField(Enseignant, blank=True, related_name="matiere_enseigne_par")
    couverture = models.ImageField(upload_to="images/", blank=True, null=True)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="matiere_created_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="matiere_updated_by")
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom_mat} - {self.classe_mat}"


class Sommaire(models.Model):
    titre = models.CharField(max_length=250)
    matiere = models.ForeignKey(Matiere, on_delete=models.SET_NULL, null=True)

    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="sommaire_created_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="sommaire_updated_by")
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.matiere} | {self.titre}"


class Cours(models.Model):
    titre = models.CharField(max_length=200)
    contenu = HTMLField()
    sommaire = models.ForeignKey(Sommaire, on_delete=models.SET_NULL, null=True)

    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="cours_created_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="cours_updated_by")
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.titre} {self.sommaire}"


class supportCours(models.Model):
    status = [
        (1, "Actif"),
        (2, "Supprimer")
    ]
    statut = models.SmallIntegerField(choices=status, default=1)
    designation_support = models.FileField(verbose_name="", upload_to="documents/")
    matiere_support = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="support_matiere")
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="support_cours_created_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   related_name="support_cours_updated_by")
    updated_at = models.DateTimeField(blank=True, null=True)
