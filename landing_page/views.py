from django.shortcuts import render


def home(request):
    return render(request, template_name="landing_page/index.html")
