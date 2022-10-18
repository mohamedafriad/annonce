from django import forms
from .models import Commentaire, Article


class CommentaireForm(forms.ModelForm):
	contenu = forms.CharField(label="Contenu", max_length=5000, required=True, widget=forms.Textarea(attrs={"rows":3,}))
	
	class Meta:
		model = Commentaire
		exclude = ['article',]