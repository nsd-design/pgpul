"""
URL configuration for pgpul_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from landing_page.views import home
from pgpul_admin.views import dashboard

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('pgpul_admin_page/', admin.site.urls),
    path('', home, name='home'),
    path('dashmin/', dashboard, name='dashmin'),
    path('dashmin/', include('landing_page.urls')),
    path('user/', include('utilisateur.urls')),
    path('', include('pgpul_admin.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
