import pathlib

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.serializers.json import DjangoJSONEncoder

from landing_page.forms import PostForm, TemoignageForm, PartenaireForm, CommentForm

from landing_page.models import Post, Temoignage, Partenaire, Comment


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

    post_form = PostForm()
    # Recuperatons des articles
    articles = Post.objects.all().order_by("-created_at")
    paginator = Paginator(articles, 6)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    context = {"form": post_form, "articles": page_object}

    return render(request, "landing_page/blog.html", context)


def lire_article(request, id_article):
    article = get_object_or_404(Post, id=int(id_article))

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = article
            new_comment.save()

            return JsonResponse({
                "success": True,
                "comment": {
                    "name": new_comment.name,
                    "content": new_comment.content,
                    "age": new_comment.age()
                }
            }, encoder=DjangoJSONEncoder)
        else:
            return JsonResponse({"success": False})

    # Get Comments by article
    comments = Comment.objects.filter(post=int(id_article)).order_by("-created_at")

    # Comment form
    comment_form = CommentForm()
    # Check if user is connected
    if request.user.username == "":
        is_not_connected = True
    else:
        is_not_connected = False
        comment_form.fields['name'].initial = request.user.username

    context = {
        "article": article,
        "comment_form": comment_form,
        "is_not_connected": is_not_connected,
        "comments": comments,
    }
    return render(request, "landing_page/lire_article.html", context)


def temoignage(request):
    temoignage_form = TemoignageForm()
    # temoignages = get_list_or_404(Temoignage)

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

    temoignages_list = Temoignage.objects.all().order_by('-id')
    paginator = Paginator(temoignages_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"form": temoignage_form,
               "page_obj": page_obj}
    return render(request, "landing_page/temoignage.html", context)


def check_file_type(file):
    extensions = ['.jpg', '.jpeg', '.png']
    # Verifier si le cover a ete soumis
    # print("\n\nFile", file)
    if file:
        # print("\n\nfichier uploaded...")
        ext = pathlib.Path(str(file)).suffix  # get file extension
        # Verifier si le type de fichier est autorisé
        if ext in extensions:
            return True
        else:
            return False


def partenaire(request):
    if request.method == "POST":
        form = PartenaireForm(request.POST, request.FILES)
        file = request.FILES.get('logo', None)
        # Verifier si le cover a ete soumis
        # print("\n\nFile", file)
        if not check_file_type(file):
            return JsonResponse({"error": "Type de fichier non autorisé"})
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.created_by = request.user
                post.save()
            except Exception as e:
                return JsonResponse({"error": True, "msg": e})
            else:
                return JsonResponse({"success": True, "msg": "Partenaire créé avec succès"})

    form = PartenaireForm()
    partenaires = Partenaire.objects.all().order_by('-created_at')
    paginator = Paginator(partenaires, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'form': form, 'partenaires': page_obj}

    return render(request, "landing_page/parteniare.html", context)
