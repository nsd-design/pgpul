from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.core.serializers import serialize
from django.db.models import Count
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from pgpul_admin.forms import *
from pgpul_admin.models import *
from pgpul_project.settings import EMAIL_HOST_USER
# from pgpul_project.settings import EMAIL_HOST_USER

from utilisateur.models import Utilisateur

template_model = "pgpul_admin/inc/"
template_path = "pgpul_admin/pages/"


def dashboard(request):
    return render(request, f'{template_model}dashboard.html')


def departement(request):
    # Les Formulaires des 3 models Faculte, Departement et Classe
    fac_form = FaculteForm()  # Formulaire pour la Faculte
    dept_form = DepartementForm()  # Formulaire pour le Departement
    classe_form = ClassForm()  # Formulaire pour le Departement
    # ==============================================

    # Generer la liste des enregistrements de Faculte, Departement et Classe
    facultes = Faculte.objects.all().order_by("code_fac")
    departements = Departement.objects.all().order_by("dept_fac")
    classes = Classe.objects.all().order_by("designation")
    

    context = {
        "fac_form": fac_form, "dept_form": dept_form, "classe_form": classe_form,
        "facultes": facultes, "departements": departements, "classes": classes
    }
    
    return render(request, template_model + "departement.html", context=context)


def create_faculte(request):
    if request.method == "POST":
        fac_code = request.POST['code_fac']

        # print("formulaire de faculte", request.POST)
        if Faculte.objects.filter(code_fac=fac_code).exists():
            return JsonResponse({"exists": "Ce code existe déjà, veuillez entrer un nouveau code de Faculté."})

        fac_form = FaculteForm(request.POST)
        if fac_form.is_valid():
            fac_name = fac_form.cleaned_data['nom_fac']
            fac_code = fac_form.cleaned_data['code_fac']
            user = request.user
            new_fac = Faculte.objects.create(
                nom_fac=fac_name, code_fac=fac_code, created_by=user
            )
            new_fac.save()
            return JsonResponse({"success": True, "msg": "Faculté créée avec succès !"})
        else:
            return JsonResponse({"errors": fac_form.errors})
    return redirect('departement')


def create_department(request):
    if request.method == "POST":
        # Verifier si ce code de Departement exist deja dans la db
        code_depart = request.POST['code_dept']
        if Departement.objects.filter(code_dept=code_depart).exists():
            return JsonResponse({"exists": "Ce code existe déjà, veuillez entrer un nouveau code de Département."})
        
        dept_form = DepartementForm(request.POST)
        if dept_form.is_valid():
            nom_dept = dept_form.cleaned_data['nom_dept']
            code_dept = dept_form.cleaned_data['code_dept']
            dept_fac = dept_form.cleaned_data['dept_fac']
            user = request.user
            new_dept = Departement.objects.create(
                nom_dept=nom_dept, code_dept=code_dept, dept_fac=dept_fac, created_by=user
            )
            new_dept.save()
            return JsonResponse({"success": True, "msg": "Département créé avec succès !"})
        else:
            return JsonResponse({"errors": dept_form.errors})

    return redirect('departement')


def create_classe(request):
    if request.method == "POST":
        # Verifier la classe existe dans la db
        nom_classe = request.POST['designation']
        if Classe.objects.filter(designation=nom_classe).exists():
            return JsonResponse({"exists": "Cette classe existe déjà, veuillez entrer une nouvelle désignation."})
        
        class_form = ClassForm(request.POST)

        if class_form.is_valid():
            user = request.user
            designation = class_form.cleaned_data['designation']

            new_class = Classe.objects.create(designation=designation, created_by=user)
            new_class.save()

            return JsonResponse({"success": True, "msg": "Classe créée avec succès !"})
        else:
            return JsonResponse({"errors": class_form.errors})

    return redirect('departement')


def create_matiere(request):
    form_matiere = MatiereForm()
    #  Liste des departements
    departements = Departement.objects.all().order_by("dept_fac")

    # Liste des matieres
    list_matieres = []
    matieres = Matiere.objects.all().order_by('dept_mat')

    for matiere in matieres:
        mat = Matiere.objects.get(pk=matiere.pk)
        enseignant = mat.enseigne_par.all()
        list_enseignant = [ens for ens in enseignant]
        current_matiere = {
            "id": matiere.id,
            "nom_mat": matiere.nom_mat,
            "classe_mat": matiere.classe_mat,
            "dept_mat": matiere.dept_mat,
            "enseigne_par": list_enseignant
        }
        list_matieres.append(current_matiere)

    #  Liste des classes
    liste_classes = get_list_or_404(Classe)

    if request.method == "POST":
        form = MatiereForm(request.POST)
        if form.is_valid():
            user = request.user
            nom_mat = form.cleaned_data['nom_mat']
            classe_mat = form.cleaned_data['classe_mat']
            dept_mat = form.cleaned_data['dept_mat']

            new_matiere = Matiere.objects.create(
                nom_mat=nom_mat, classe_mat=classe_mat, dept_mat=dept_mat, created_by=user
            )

            new_matiere.save()
            return JsonResponse({"success": True, "msg": "La matièere a été créée avec succès !"})
        else:
            return JsonResponse({"errors": form.errors})
    form_sommaire = SommaireForm()
    context = {"form": form_matiere, "matieres": list_matieres, "departements": departements,
               "liste_classes": liste_classes, "form_sommaire": form_sommaire}
    return render(request, template_model+"matiere.html", context=context)


def matiere_par_departement(request):
    if request.method == "GET":
        # Recuperer les id dans le param GET
        id_dept = request.GET.get('departement')
        id_classe = request.GET.get('classe')

        id_classe = id_classe if id_classe != -1 else 0

        matiere_par_dept = Matiere.objects.filter(dept_mat=id_dept, classe_mat=id_classe)
        enseignants = get_list_or_404(Enseignant)
        liste_matieres = [{'id': matiere.id, 'matiere': matiere.nom_mat} for matiere in matiere_par_dept]

        liste_enseignants = [
            {
                'id': enseignant.id,
                'username': enseignant.username,
                'first_name': enseignant.first_name,
                'last_name': enseignant.last_name,
                'departement_principal': enseignant.departement_principal.nom_dept,
            }
            for enseignant in enseignants
        ]
        liste_matieres = liste_matieres if liste_matieres else None
        liste_enseignants = liste_enseignants if liste_enseignants else None
    return JsonResponse({"liste_matieres": liste_matieres, "liste_enseignants": liste_enseignants})


def attribuer_matiere_a_pro(request):
    if request.method == "POST":
        id_matiere = request.POST['matiere']
        enseignant = request.POST.getlist('enseignant')

        if id_matiere and len(enseignant) > 0:
            matiere = Matiere.objects.get(id=id_matiere)
            if matiere:
                matiere.enseigne_par.set(enseignant)
                matiere.save()
                print("attribution effectuéee")
                messages.success(request, "Attribution effectué avec succès")

    return redirect("matiere")


def enseignant(request):
    form = EnseignantForm()
    enseignants = Enseignant.objects.all().order_by('last_name')
    if request.method == "POST":
        form = EnseignantForm(request.POST)
        if form.is_valid():
            user = request.user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            tel = form.cleaned_data['tel_ens']
            sepecialite = form.cleaned_data['specialite_ens']
            departement_principal = form.cleaned_data['departement_principal']
            adresse_en = form.cleaned_data['adresse_en']
            genre_ens = form.cleaned_data['genre_ens']

            new_enseignant = Enseignant.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                tel_ens=tel,
                specialite_ens=sepecialite,
                departement_principal=departement_principal,
                adresse_en=adresse_en,
                genre_ens=genre_ens,
                created_by=user
            )
            new_enseignant.save()

            send_confirmation_email(request, new_enseignant)

            return JsonResponse({"success": True, "msg": "Enseignant enregistré avec succès !"})
        else:
            return JsonResponse({"errors": form.errors})

    context = {"form": form, "enseignants": enseignants}
    return render(request, template_path+"enseignant.html", context=context)


def liste_enseignants(request):
    if request.method == "GET":
        liste_des_enseignants = []
        enseignants = Enseignant.objects.all()
        for ens in enseignants:
            teacher = {
                'id': ens.id,
                'first_name': ens.first_name,
                'last_name': ens.last_name,
                'email': ens.email,
                'username': ens.username,
                'tel_ens': ens.tel_ens,
                'specialite_ens': ens.specialite_ens,
                'departement_principal': ens.departement_principal.nom_dept,
                'adresse_en': ens.adresse_en,
                'genre_ens': ens.genre_ens
            }
            liste_des_enseignants.append(teacher)
        return JsonResponse({"liste_enseignants": liste_des_enseignants})


def create_etudiant(request):
    form = EtudiantForm()

    if request.method == "POST":
        form_etd = EtudiantForm(request.POST)
        if form_etd.is_valid():
            first_name = form_etd.cleaned_data['first_name']
            last_name = form_etd.cleaned_data['last_name']
            username = form_etd.cleaned_data['username']
            matricule = form_etd.cleaned_data['matricule']
            genre_etd = form_etd.cleaned_data['genre_etd']
            tel_etd = form_etd.cleaned_data['tel_etd']
            departement_etd = form_etd.cleaned_data['departement_etd']
            email_etd = form_etd.cleaned_data['email']

            user = request.user
            try:
                new_etudiant = Etudiant.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email_etd,
                    username=username,
                    matricule=matricule,
                    genre_etd=genre_etd,
                    tel_etd=tel_etd,
                    departement_etd=departement_etd,
                    created_by=user
                )
                message = "Ce mail a ete envoye pour tester la creation d'etudiant"
                recipients = ["ibayotech@gmail.com"]
                # send_mail = EmailMessage(
                #     subject="Test envoie mail etudiant",
                #     body=message,
                #     from_email=EMAIL_HOST_USER,
                #     to=recipients,
                # )
                # send_mail.send(fail_silently=False)
                new_etudiant.save()

                send_confirmation_email(request, new_etudiant)

            except Exception as e:
                print("Failed to send", e)
                JsonResponse({'errors': f"Erreur lors de la creation de l'etudiant: {str(e)}"})
            else:
                # new_etudiant.save()
                #  app password: xnunfvgdywbexpfn
                message = "Ce mail a ete envoye pour tester la creation d'etudiant"
                recipients = ["ibayotech@gmail.com"]
                try:
                    # send_mail(
                    #     subject="Test envoie mail etudiant",
                    #     message=message,
                    #     from_email="",
                    #     recipient_list=recipients,
                    # )
                    pass
                except Exception as e:
                    print("Error envoie mail", e)
                return JsonResponse({'success': True, "msg": "Etudiant enregistré avec succès !"})
        else:
            return JsonResponse({'errors': form_etd.errors})
    context = {'form': form}
    return render(request, template_path+"etudiant.html", context=context)


def send_confirmation_email(request: HttpRequest, utilisateur):
    user_info_link = "/compte/confirmation/" + str(utilisateur.id) + "/"

    #  Creer le lien absolue du template devant etre afficher pour la confirmation du compte
    absolut_confirmation_link = request.build_absolute_uri(user_info_link)

    subject = "Confirmation de compte"
    html_message = render_to_string(template_path + "confirmation_email_template.html",
                                    {"etudiant": utilisateur, "confirmation_link": absolut_confirmation_link})
    plain_message = strip_tags(html_message)
    print("utilisateur/destinateur", utilisateur)
    mail_sent = send_mail(
        subject=subject, message=plain_message,
        from_email=EMAIL_HOST_USER, recipient_list=[utilisateur.email],
        fail_silently=False, html_message=html_message
    )


def get_user_infos(request, id_utilisateur):
    if request.method == 'GET':
        utilisateur = get_object_or_404(Utilisateur, id=id_utilisateur)

        context = {"id": id_utilisateur, "username": utilisateur.username, "pwd": utilisateur.password}

        return render(request, template_path+"confirmation_compte.html", context=context)


def liste_etudiants(request):
    if request.method == "GET":
        etudiants = Etudiant.objects.all().order_by('departement_etd')
        json_data = serialize('json', etudiants)

        list_etudiants = [{'first_name': etd.first_name, 'last_name': etd.last_name,
                           'usemail': etd.username, 'matricule': etd.matricule,
                           'genre_etd': etd.get_genre_etd_display(), 'tel_etd': etd.tel_etd,
                           'departement_etd': etd.departement_etd.nom_dept
                           } for etd in etudiants]

        return JsonResponse({"list_etudiants": list_etudiants})


def cours(request):
    form = CoursForm()

    if request.method == 'POST':
        sommaire_id = request.POST.get('sommaire')

        sommaire = Sommaire.objects.get(id=int(sommaire_id))
        if not sommaire:
            return JsonResponse({"error": True, "msg": "Ce chapitre n'existe pas dans la table des matieres"})

        titre = request.POST.get('titre')
        contenu = request.POST.get('contenu')

        new_course = Cours.objects.create(
            titre=titre, contenu=contenu, sommaire=sommaire, created_by=request.user
        )
        new_course.save()

        # list_cours = Cours.objects.all()
        # context = {"form": form, "list_cours": list_cours}
        return JsonResponse({"success": True})


def create_sommaire(request):
    form = SommaireForm()
    if request.method == "POST":
        id_matiere = request.POST["id-de-la-matiere"]

        if id_matiere:
            try:
                matiere = Matiere.objects.get(id=id_matiere)

                titres = request.POST.getlist("titre")

                for titre in titres:
                    new_sommaire = Sommaire.objects.create(
                        titre=titre, matiere=matiere, created_by=request.user
                    )
                    new_sommaire.save()
            except Exception:
                return JsonResponse({"errors": True, "msg": "Erreur lors de la creation"})
        else:
            return JsonResponse({"errors": True, "msg": "Veuillez specifier une matiere"})

        return JsonResponse({"success": True, "msg": "Nouveau chapitre ajouté à la table des matières avec succès"})
    context = {"form": form}
    return render(request, template_path+"sommaire.html", context=context)


def afficher_table_matieres(request, id_matiere):
    if request.method == "GET":
        form = CoursForm()

        id_matiere = int(id_matiere)
        nom_matiere = Matiere.objects.get(id=id_matiere)
        sommaire_maitere = Sommaire.objects.filter(id=id_matiere)

        context = {"form": form, "sommaire_maitere": sommaire_maitere, "nom_matiere": nom_matiere}
        return render(request, template_path+"table_des_matieres.html", context=context)


def liste_des_matieres(request):
    user = request.user
    liste_cours = ""
    #  Si user est un enseignant
    liste_cours = Cours.objects.filter(created_by=user)
    # print("liste cours", liste_cours)

    #  Si user est un etudiant
    dept_etd = Etudiant.objects.get(id=7)
    departement = dept_etd.departement_etd
    matieres_by_departement = Matiere.objects.filter(dept_mat=departement)

    #  Recuperer les matieres et les enseignants qui enseignent chacune des matieres
    list_matieres = []
    for matiere in matieres_by_departement:
        mat = Matiere.objects.get(pk=matiere.pk)
        enseignant = mat.enseigne_par.all()
        list_enseignant = [ens for ens in enseignant]
        current_matiere = {
            "id_matiere": matiere.id,
            "nom_mat": matiere.nom_mat,
            "enseigne_par": list_enseignant,
        }
        list_matieres.append(current_matiere)
    context = {"list_matieres": list_matieres, "departement": departement.nom_dept}
    return render(request, template_path+"liste_des_matieres.html", context)


def sommaire_par_matiere(request, id_matiere):
    sommaire_matiere = Sommaire.objects.filter(matiere=id_matiere)
    matiere = Matiere.objects.get(id=id_matiere)
    titres_cours = []

    for sommaire in sommaire_matiere:
        liste_cours = Cours.objects.filter(sommaire=sommaire)
        current_sommaire = {
            "sommaire": sommaire.id,
            "sommaire_titre": sommaire.titre,
            "titre_cours": [current_cours for current_cours in liste_cours]
        }
        titres_cours.append(current_sommaire)
    context = {"sommaire_et_cours": titres_cours, "matiere": matiere}
    return render(request, template_path+"sommaire_par_matiere.html", context)


def affiche_contenu_cours(request, id_cours, id_matiere):

    cours = Cours.objects.get(id=id_cours)

    context = {'cours': cours, 'id_matiere': id_matiere}
    return render(request, template_path+"cours.html", context)


def create_support_cours(request):
    form = SupportCoursForm()

    if request.method == "POST":
        support_form = SupportCoursForm(request.POST, request.FILES)

        if support_form.is_valid():
            document = support_form.cleaned_data['designation_support']
            matiere = support_form.cleaned_data['matiere_support']

            new_support = supportCours.objects.create(
                designation_support=document, matiere_support=matiere, created_by=request.user
            )

            new_support.save()
            messages.success(request, "Support de cours enregistré avec succès !")
        return redirect("support_cours")
    context = {'form': form}
    return render(request, template_path + "support_cours.html", context)
