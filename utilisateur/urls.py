from django.urls import path

from utilisateur.views import inscription, connexion

urlpatterns = [
    path('signup/', inscription, name='inscription'),
    path('login/', connexion, name='connexion')
]
