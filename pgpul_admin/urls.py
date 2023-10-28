from django.urls import path

from pgpul_admin.views import departement, create_faculte, create_department

urlpatterns = [
    path("departement/", departement, name="departement"),
    path("departement/fac/", create_faculte, name="fac"),
    path("departement/dept/", create_department, name="dept"),
]
