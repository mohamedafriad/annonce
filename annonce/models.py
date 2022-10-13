from django.db import models
from django.contrib.auth.models import Group, User


FORME_JURIDIQUE = (
    (1, "Personne physique"),
    (2, "Auto-entrepreneur"),
    (3, "SARL"),
    (4, "SARLAU"),
    (5, "SNC"),
    (6, "SCS"),
    (7, "SCA"),
    (8, "Société Annonyme Simplifiée (SAS)"),
    (9, "Société Annonyme (SA)"),
    (10, "Groupement d'Intérêt Economique (GIE)"),
)
class Entreprise(models.Model):
    denomination = models.CharField("Dénomination", max_length=500)
    raison_soc = models.CharField("Raison sociale", max_length=500)
    statut  = models.CharField("Statut juridique", max_length=50, blank=True)
    rc = models.CharField("N° de RC", max_length=50, blank=True)
    ice = models.CharField("N° de ICE", max_length=50, blank=True)
    activite = models.CharField("Activité", max_length=500, blank=True)
    forme = models.PositiveSmallIntegerField("Forme juridique", choices=FORME_JURIDIQUE, default = 1)
    date_immatriculation = models.DateField("Date d'immatriculation", null=True, blank=True)
    capital = models.DecimalField("Capital (en MAD)", max_digits=20, decimal_places=2)
    tribunal = models.CharField("Tribunal", max_length=250, blank=True)
    ville = models.CharField("Ville", max_length=250, blank=True)
    adresse = models.CharField("Adresse", max_length=500, blank=True)
    longitude = models.CharField("longitude", max_length=50, blank=True)
    latitude = models.CharField("latitude", max_length=50, blank=True)
    fixe = models.CharField("Fixe", max_length=50, blank=True)
    fax = models.CharField("Fax", max_length=50, blank=True)
    email = models.CharField("Email", max_length=50, blank=True)
    representant = models.CharField("Représentant", max_length=250, blank=True)
    gerant = models.CharField("Gérant", max_length=250, blank=True)

    def __str__(self):
        return self.denomination

    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, related_name="users", null=True)
    date_inscription = models.DateField("Date inscription", blank=True, null=True)


    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"


ETAT_ANNONCE = (
    (1, "En attente"),
    (2, "Publiée"),
    (3, "Rejetée"),
)
TYPE_ANNONCE=(
    (1, "Constitution"),
    (2, "Dissolution"),
    (3, "Clôture de la liquidation"),
    (4, "Continuité de l'ativité"),
    (5, "Changement de dirigeant"),
    (6, "Transfert de siège social"),
    (7, "Changement d'objet social"),
    (8, "Changement de dénomination"),
    (9, "Tranformation de la forme sociale"),
    (10, "Cession de parts sociales"),
    (11, "Réduction de capital"),
    (12, "Augmentation de capital"),
)
CATEGORIE_ANNONCE=(
    (1, "Constitution"),
    (2, "Cessation d'activité"),
    (3, "Modification de société"),
)

class Annonce(models.Model):
    reference = models.CharField("Référence", max_length=200)
    intitule = models.CharField("Intitule", max_length=250)
    date_creation = models.DateTimeField("Date création", auto_now=False, auto_now_add=True)
    date_publication = models.DateField("Date publication", auto_now=False, auto_now_add=False, null=True, blank=True)
    contenu = models.CharField("Contenu", max_length=1000)
    etat = models.PositiveSmallIntegerField("Etat", choices=ETAT_ANNONCE, default = 1)
    categorie = models.PositiveSmallIntegerField("Catégorie", choices=CATEGORIE_ANNONCE, default = 1)
    type_annonce = models.PositiveSmallIntegerField("Type", choices=TYPE_ANNONCE, default = 1)
    annonceur = models.ForeignKey(Profil, on_delete=models.SET_NULL, related_name="annonces", null=True)

    
    def __str__(self) :
        return self.intitule
    
    class Meta:
        verbose_name = "Annonce"
        verbose_name_plural = "Annonces"