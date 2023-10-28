from django.http import JsonResponse
from django.shortcuts import render, redirect

from pgpul_admin.forms import *
from pgpul_admin.models import *

template_model = "pgpul_admin/inc/"


def dashboard(request):
    return render(request, f'{template_model}dashboard.html')


def departement(request):
    fac_form = FaculteForm()  # Formulaire pour la Faculte
    dept_form = DepartementForm()  # Formulaire pour le Departement
    classe_form = ClassForm()  # Formulaire pour le Departement

    context = {"fac_form": fac_form, "dept_form": dept_form, "classe_form": classe_form}
    
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
