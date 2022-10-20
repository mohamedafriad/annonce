from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from .models import Entreprise, Annonce, Profil


class GroupAdmin(BaseGroupAdmin):
    save_as = True


class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('reference', 'intitule', 'date_creation', 'date_publication', 'get_etat_display')

admin.site.register(Entreprise)
admin.site.register(Annonce, AnnonceAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Profil)