from django.urls import path

from utilisateur.views import *
urlpatterns = [
    path('signup/', inscription, name='signup'),
    path('login/', connexion, name='connexion'),
    path('logout/', deconnexion, name='deconnexion'),
    path('confirmation/', confirmation_compte, name='confirmation_compte'),
]
