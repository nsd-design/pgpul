from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def home(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Vous êtes connecté avec succès !")
            return redirect('dashmin')
        else:
            messages.error(request, "Identifiants incorrects. Veuillez réessayer.")

    return render(request, template_name="landing_page/index.html")
