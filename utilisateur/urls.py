from django.urls import path

from utilisateur.views import inscription, connexion, deconnexion

urlpatterns = [
    path('signup/', inscription, name='signup'),
    path('login/', connexion, name='connexion'),
    path('logout/', deconnexion, name='deconnexion'),
]
