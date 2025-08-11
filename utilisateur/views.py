from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# from pgpul_admin.forms import InscriptionForm
from utilisateur.models import Utilisateur

# Nom de l'applicaton du Template
temp = "utilisateur/"


def connexion(request):
    if request.method == "POST":
        username_or_email = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Vous êtes connecté avec succès !")
            return redirect('dashmin')
        else:
            messages.error(request, "Identifiants incorrects. Veuillez réessayer.")
    return render(request, temp+"connexion.html")


@login_required(login_url="connexion")
def deconnexion(request):
    logout(request)
    return redirect('connexion')


def inscription(request):
    pass
    # if request.method == "POST":
    #
    #     form = InscriptionForm(request.POST)
    #
    #     if form.is_valid():
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         email = form.cleaned_data['email']
    #         password = form.cleaned_data['password']
    #         matricule = form.cleaned_data['matricule']
    #         username = form.cleaned_data['username']
    #
    #         confirm_password = request.POST['confirm_password']
    #         if password == confirm_password:
    #             new_user = Utilisateur.objects.create_user(
    #                 first_name=first_name, last_name=last_name, email=email,
    #                 password=password, matricule=matricule, username=username
    #             )
    #             new_user.save()
    #             messages.success(request, "Votre compte a été créé avec succès !")
    #             return JsonResponse({'success': "Votre compte a été créé avec succès !"})
    #         else:
    #             messages.error(request, "Les deux mots de passe doivent être identiques")
    #             return JsonResponse({'errors': 'Erreur de mot de passe'})
    #     else:
    #         messages.error(request, "Veuillez renseigner tous les champs du formulaire")
    #         print("Error", form.errors)
    #         return JsonResponse({'errors': "Veuillez renseigner tous les champs du formulaire"})
    #
    # else:
    #     form = InscriptionForm()
    #     return render(request, temp+"inscription.html", context={'form': form})


def confirmation_compte(request):
    if request.method == 'POST':
        id_user = request.POST.get('id_user')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not password or not confirm_password:
            return JsonResponse({"errors": True, "msg": "Veillez saisire un mot de passe"})

        if password == confirm_password:

            utilisateur = Utilisateur.objects.get(id=id_user)

            try:
                utilisateur.username = username
                utilisateur.set_password(password)
                utilisateur.is_active = True
                utilisateur.save()
            except Exception as e:
                return JsonResponse({"errors": True, "msg": "Impossible de confirmer votre compte"})
            else:
                return JsonResponse({"success": True, "msg": "Votre compte a été confirmé avec succès"})
        else:
            return JsonResponse({"errors": True, "msg": "Les deux mots de passe doivent être identiques"})