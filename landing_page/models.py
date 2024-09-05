from datetime import timedelta

from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField

from utilisateur.models import Utilisateur


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = HTMLField()
    cover = models.ImageField(upload_to="images/post-covers", blank=True, null=True)
    posted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.pk} - {self.title}"

    def age(self):
        now = timezone.now()
        difference = now - self.created_at

        # Détermine combien de jours se sont écoulés
        if difference < timedelta(minutes=1):
            return "à l'instant"
        elif difference < timedelta(hours=1):
            minutes = difference.seconds // 60
            return f"il y a {minutes} minute(s)"
        elif difference < timedelta(days=1):
            hours = difference.seconds // 3600
            return f"il y a {hours} heure(s)"
        elif difference < timedelta(days=7):
            days = difference.days
            return f"il y a {days} jour(s)"
        else:
            return f"le {self.created_at.strftime('%d %B %Y')}"


class Comment(models.Model):
    name = models.CharField(max_length=125)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, null=True)


class Partenaire(models.Model):
    denomination = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="logo_partner/")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)


class Temoignage(models.Model):
    nom = models.CharField(max_length=120)
    avis = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)


class ContactUs(models.Model):
    email = models.CharField(max_length=200)
    objet = models.CharField(max_length=120)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
