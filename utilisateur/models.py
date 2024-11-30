from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    USER_TYPE_CHOICES = (
        ('etudiant', 'Étudiant'),
        ('enseignant', 'Enseignant'),
    )
    username = models.CharField(max_length=150, unique=True, blank=False)
    is_active = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.user_type}"
