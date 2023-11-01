from django.contrib.auth.models import AbstractUser
from django.db import models

from pgpul_admin.models import Departement


class Utilisateur(AbstractUser):
    matricule = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=150, unique=True, blank=False)
    photos = models.ImageField(upload_to="images", null=True, blank=True)
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
