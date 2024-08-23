from django.db import models
from tinymce.models import HTMLField

from utilisateur.models import Utilisateur


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)


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
