from django.urls import path

from landing_page.views import *

urlpatterns = [
    path('blog/', blog, name='blog'),
    path('blog/read/<int:id_article>', lire_article, name='read-article'),
    # path('blog/comment/', post_comment, name='comment'),
    path('temoignage/', temoignage, name="temoignage"),
    path('partenaire/', partenaire, name="partenaire"),
    path('partenaire/<int:id_partner>', partenaire, name="partenaire"),
]
