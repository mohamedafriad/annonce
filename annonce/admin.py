from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from .models import Entreprise, Annonce, Profil


class GroupAdmin(BaseGroupAdmin):
    save_as = True

admin.site.register(Entreprise)
admin.site.register(Annonce)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Profil)