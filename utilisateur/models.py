from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.db import models


class Utilisateur(AbstractUser):
    USER_TYPE_CHOICES = (
        ('etudiant', 'Étudiant'),
        ('enseignant', 'Enseignant'),
    )
    username = models.CharField(max_length=150, unique=True, blank=False)
    is_active = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    mot_de_passe = models.CharField(max_length=128, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):  # éviter de re-hasher
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.user_type}"
