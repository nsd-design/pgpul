from django.shortcuts import render


# Nom de l'applicaton du Template
temp = "utilisateur/"


def inscription(request):
    return render(request, temp+"inscription.html")


def connexion(request):
    return render(request, temp+"connexion.html")
