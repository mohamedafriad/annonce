from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StructureConfig(AppConfig):
    name = 'structure'
    verbose_name=_('structures')
