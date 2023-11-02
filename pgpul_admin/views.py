from django.http import JsonResponse
from django.shortcuts import render, redirect, get_list_or_404

from pgpul_admin.forms import *
from pgpul_admin.models import *

from utilisateur.models import Utilisateur

template_model = "pgpul_admin/inc/"


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

