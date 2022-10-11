from django.contrib import admin
from .models import Region, Province, Commune, Membre
from annonces.actions import export_as_xls
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

class ProvinceInline(admin.StackedInline):
    model = Province


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    search_fields = ('nom',)
    inlines = [ProvinceInline]


class CommuneInline(admin.StackedInline):
    model = Commune

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'region')
    search_fields = ('nom',)
    list_filter = ('region',)
    #autocomplete_fields = ('region',)
    inlines = [CommuneInline]


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'region', 'province', 'milieu')
    list_editable = ( 'region', 'province', 'milieu')
    list_filter = ( 'region', 'province', 'milieu')
    #autocomplete_fields = ('region', 'province')
    search_fields = ('nom',)


class GroupAdmin(BaseGroupAdmin):
    save_as = True


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Membre)