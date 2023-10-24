from django.urls import path

from utilisateur.views import inscription, connexion

urlpatterns = [
    path('signup/', inscription, name='signup'),
    path('login/', connexion, name='connexion'),
    path('logout/', connexion, name='deconnexion'),
]
