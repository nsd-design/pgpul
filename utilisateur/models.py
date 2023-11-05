from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
