from django.urls import path

from utilisateur.views import connexion, deconnexion, inscription
urlpatterns = [
    path('signup/', inscription, name='signup'),
    path('login/', connexion, name='connexion'),
    path('logout/', deconnexion, name='deconnexion'),
]
