from django.shortcuts import render


template_model = "pgpul_admin/inc/"


def dashboard(request):
    return render(request, f'{template_model}dashboard.html')
