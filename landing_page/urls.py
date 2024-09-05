from django.urls import path

from landing_page.views import *

urlpatterns = [
    path('blog/', blog, name='blog'),
    path('blog/read/<int:id_article>', lire_article, name='read-article'),
    path('temoignage', temoignage, name="temoignage")
]
