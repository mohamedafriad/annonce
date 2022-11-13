"""frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers
from frontend import views as front_views
from django.conf import settings

admin.site.enable_nav_sidebar = False

if not settings.DEBUG :
    handler404 = 'frontend.views.not_found_view'
    handler500 = 'frontend.views.not_found_view'
else:
    pass

urlpatterns = [
    path('', front_views.actualite, name="front"),
    path('backend/login/', front_views.backlogin, name="b-login"),   # connexion
    path('backend/logout/', front_views.backlogout, name="b-logout"),   # deconnexion
    path('contact/', front_views.contact, name="contact"),   # contact
    path('actualite/', front_views.actualite, name="actualite"),   # actualite
    path('actualite/article/<pk>/', front_views.article, name="article"),   # article
    path('actualite/article/<pk>/commenter/', front_views.commenter, name="commenter"),   # commenter
    path('annuaire/', front_views.annuaire, name="annuaire"),   # actualite
    path('tdb/', front_views.tdb, name="tdb"),   # tdb
    path('profil/', front_views.profil, name="profil"),   # tdb
    path('packs/', front_views.packs, name="packs"),   # tdb
    path('annonces/', front_views.liste_annonces, name="liste_annonces"),   # liste annonces
    path('annonce/nouvelle/', front_views.nouvelle_annonce, name="nouvelle_annonce"),   # nouvelle annonce    
    path('annonces/user/', front_views.user_annonces, name="mes_annonces"),   # mes annonces
    path('annonces/journal/', front_views.journal, name="journal"),
]