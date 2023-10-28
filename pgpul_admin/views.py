from django.http import JsonResponse
from django.shortcuts import render, redirect

from pgpul_admin.forms import FaculteForm
from pgpul_admin.models import Faculte

template_model = "pgpul_admin/inc/"


def dashboard(request):
    return render(request, f'{template_model}dashboard.html')


def departement(request):
    fac_form = FaculteForm()
    return render(request, template_model + "departement.html",
                  context={"fac_form": fac_form})


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

            new_fac = Faculte.objects.create(
                nom_fac=fac_name, code_fac=fac_code
            )
            new_fac.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"errors": fac_form.errors})
    return redirect('departement')
