from django.http import JsonResponse
from django.shortcuts import render, redirect, get_list_or_404

from pgpul_admin.forms import *
from pgpul_admin.models import *

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

        print("formulaire de faculte", request.POST)
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
            return JsonResponse({"success": True})
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
            return JsonResponse({"success": True})
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

            return JsonResponse({"success": True})
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
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"errors": form.errors})
    context = {"form": form_matiere, "matieres": list_matieres, "departements": departements,
               "liste_classes": liste_classes}
    return render(request, template_model+"matiere.html", context=context)


def matiere_par_departement(request):
    if request.method == "GET":
        # Recuperer les id dans le param GET
        id_dept = request.GET.get('departement')
        id_classe = request.GET.get('classe')

        id_classe = id_classe if id_classe != -1 else 0

        matiere_par_dept = Matiere.objects.filter(dept_mat=id_dept, classe_mat=id_classe)
        enseignant_par_dept = get_list_or_404(Utilisateur, departement=id_dept)
        liste_matieres = dict([(matiere.id, matiere.nom_mat) for matiere in matiere_par_dept])

        liste_enseignants = [
            {
                'id': enseignant.id,
                'username': enseignant.username,
                'first_name': enseignant.first_name,
                'last_name': enseignant.last_name
            }
            for enseignant in enseignant_par_dept
        ]
        liste_matieres = liste_matieres if liste_matieres else None
        liste_enseignants = liste_enseignants if liste_enseignants else None
    return JsonResponse({"liste_matieres": liste_matieres, "liste_enseignants": liste_enseignants})


def attribuer_matiere_a_pro(request):
    if request.method == "POST":
        departements = request.POST['departement']
        classe = request.POST['classe']
        id_matiere = request.POST['matiere']
        enseignant = request.POST.getlist('enseignant')

        if id_matiere and len(enseignant) > 0:
            matiere = Matiere.objects.get(id=id_matiere)
            if matiere:
                matiere.enseigne_par.set(enseignant)
                matiere.save()
                print("attribution effectuéee")

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
            return JsonResponse({"success": True})
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
