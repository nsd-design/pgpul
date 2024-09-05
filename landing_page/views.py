import pathlib

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from landing_page.forms import PostForm, TemoignageForm
from landing_page.models import Post, Temoignage


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
    # Recuperatons des articles
    articles = Post.objects.all()
    context = {"form": post_form, "articles": articles}

    # Creation d'un article
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
                # print("Post saved")
                return JsonResponse({"success": True, "msg": "Article créé avec succès"})

    return render(request, "landing_page/blog.html", context)


def lire_article(request, id_article):
    if request.method == "GET":
        article = get_object_or_404(Post, id=int(id_article))
        # print("Article:", article)
        context = {"article": article}
        return render(request, "landing_page/lire_article.html", context)


def temoignage(request):
    temoignage_form = TemoignageForm()
    temoignages = get_list_or_404(Temoignage)
    context = {"form": temoignage_form,
               "temoignages": temoignages}

    if request.method == "POST":
        temoignage_form = TemoignageForm(request.POST)
        if temoignage_form.is_valid():
            nom = temoignage_form.cleaned_data['nom']
            avis = temoignage_form.cleaned_data['avis']

            try:
                user = request.user
                temoignage_et = Temoignage.objects.create(nom=nom, avis=avis, created_by=user)
            except Exception as e:
                print(e)
            else:
                temoignage_et.save()
                return JsonResponse({"success": True, "msg": "Merci pour votre temoignage"})

    return render(request, "landing_page/temoignage.html", context)
