from django.db import models

from django.conf import settings
# from utilisateur.models import Utilisateur

Utilisateur = settings.AUTH_USER_MODEL


class UserInfos(models.Model):
    status = [
        (1, "Actif"),
        (2, "Supprimer")
    ]
    statut = models.SmallIntegerField(choices=status, default=1)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL,
                                   null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   blank=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Enseignant(Utilisateur):
    gender = [
        (1, "Féminin"),
        (2, "Masculin"),
    ]
    genre_ens = models.SmallIntegerField(choices=gender)
    tel_ens = models.CharField(max_length=12)
    specialite_ens = models.CharField(max_length=40)
    adresse_en = models.CharField(max_length=30)
    photo_ens = models.ImageField(upload_to="images", blank=True, null=True)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL,
                                   null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   blank=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Faculte(UserInfos):
    nom_fac = models.CharField(max_length=50)
    code_fac = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.nom_fac}"


class Departement(UserInfos):
    nom_dept = models.CharField(max_length=50)
    code_dept = models.IntegerField(unique=True)
    dept_fac = models.ForeignKey(Faculte, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom_dept} - {self.code_dept}"


class Etudiant(Utilisateur):
    gender = [
        (1, "Féminin"),
        (2, "Masculin"),
    ]
    matricule = models.CharField(max_length=15, unique=True)
    genre_etd = models.SmallIntegerField(choices=gender)
    tel_etd = models.CharField(max_length=12)
    departement_etd = models.ForeignKey(Departement, on_delete=models.CASCADE)
    photo_ens = models.ImageField(upload_to="images", blank=True, null=True)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL,
                                   null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True,
                                   blank=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.matricule}"


class Classe(UserInfos):
    designation = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f"{self.designation}"


class Matiere(UserInfos):
    nom_mat = models.CharField(max_length=40)
    classe_mat = models.ForeignKey(Classe, on_delete=models.CASCADE)
    dept_mat = models.ForeignKey(Departement, on_delete=models.CASCADE)
    enseigne_par = models.ManyToManyField(Enseignant, blank=True)

    def __str__(self):
        return f"{self.nom_mat} - {self.classe_mat}"


class supportCours(UserInfos):
    designation_support = models.FileField(verbose_name="", upload_to="documents")
    matiere_support = models.ForeignKey(Matiere, on_delete=models.CASCADE)
