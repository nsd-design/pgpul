import pathlib

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect

from landing_page.forms import PostForm


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


def blog(request):
    post_form = PostForm()
    context = {"form": post_form}
    if request.method == "POST":
        extensions = ['.jpg', '.jpeg', '.png']
        form = PostForm(request.POST, request.FILES)
        file = request.FILES.get('cover', None)
        # Verifier si le cover a ete soumis
        # print("\n\nFile", file)
        if file:
            # print("\n\nfichier uploaded...")
            ext = pathlib.Path(str(file)).suffix  # get file extension
            # Verifier si le type de fichier est autorisé
            if ext not in extensions:
                return JsonResponse({"error": "Type de fichier non autorisé"})
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.created_by = request.user
                post.save()
            except Exception as e:
                return JsonResponse({"error": True, "msg": e})
            else:
                print("Post saved")
                return JsonResponse({"success": True, "msg": "Article créé avec succès"})

    return render(request, "landing_page/blog.html", context)
