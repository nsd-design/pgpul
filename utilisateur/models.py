from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    matricule = models.CharField(max_length=15)
    photos = models.ImageField(upload_to="images", null=True, blank=True)
