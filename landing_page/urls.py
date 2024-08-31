from django.urls import path

from landing_page.views import *

urlpatterns = [
    path('blog/', blog, name='blog')
]