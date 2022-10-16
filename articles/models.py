from django.db import models

class Article(models.Model):
	titre  = models.CharField("Titre", max_length=500)
	auteur = models.CharField("Auteur", max_length=500, null=True, blank=True)
	journal = models.CharField("Journal", max_length=250, null=True, blank=True)
	date_creation = models.DateField("Date Création", null=True, blank=True)
	date_publication = models.DateField("Date Publication", null=True, blank=True)
	contenu = models.CharField("Contenu", max_length=5000)
	tags = models.CharField("Mots clés", max_length=250, blank=True)
	image = models.URLField("Affiche", blank=True, null=True)
	url = models.URLField("Lien", blank=True, null=True)
	categorie = models.CharField("Catégorie", max_length=50, blank=True)

	def __str__(self):
		return self.titre

	class Meta:
		verbose_name ="Article"
		verbose_name_plural = "Articles"
