from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import Entreprise, Profil, Annonce

class EntrepriseForm(forms.ModelForm):

	class Meta:
		model = Entreprise
		fields = '__all__'


class AnnonceForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			FloatingField('intitule', 'date_creation'),
		)

	class Meta:
		model = Annonce
		exclude = ['reference', 'annonceur', 'etat',]
		widgets = {
		  'contenu': forms.Textarea(attrs={'rows':2, 'cols':20}),
		}
	