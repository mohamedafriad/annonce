from django.db import models


class Annonce(models.Model):
    reference = models.CharField("Référence", max_length=200)
    intitule = models.CharField("Intitule", max_length=250)
    date_creation = models.DateTimeField("Date création", auto_now=False, auto_now_add=True)
    date_publication = models.DateField("Date publication", auto_now=False, auto_now_add=False, null=True, blank=True)
    annonceur = models.CharField("Annonceur", max_length=500)
    contenu = models.CharField("Contenu", max_length=1000)
    etat = models.PositiveSmallIntegerField("Etat", default = 1)
    categorie = models.CharField("Catégorie", max_length=500)
    type = models.PositiveSmallIntegerField("Type", default=1)
    
    def __str__(self) :
        return self.intitule
    
    class Meta:
        verbose_name = "Annonce"
        verbose_name_plural = "Annonces"