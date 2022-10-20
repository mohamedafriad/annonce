from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse
from structure.models import Province, Region, Commune
from .forms import LoginForm, ContactForm
from annonce.models import Entreprise, Annonce, Profil
from annonce.forms import EntrepriseForm, AnnonceForm
from articles.models import Article
from articles.forms import CommentaireForm	

# view de connexion : OK
def backlogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None: #utilisateur existe
                login(request, user)
                return redirect('tdb') # redirection vers le tableau de bord
            else:  # # identifiants erronés : utilisateur n'existe pas
                messages.add_message(request, messages.ERROR, "erreur d'authentification")
                request.session["page_active"]=0 # page de connexion active
                return redirect('b-login')
        else:  # formulaire non valide
            messages.add_message(request, messages.ERROR, "erreur d'authentification")
            request.session["page_active"]=0 # page de connexion active
            return redirect('b-login') 
    else: # method GET
        request.session["page_active"]=0 # page de connexion active
        return render(request, template_name="backend/login.html")

# view de deconnexion : OK
def backlogout(request):
    logout(request)
    request.session["page_active"]=1 # page d'accueil active
    return redirect('front') # redirection vers page accueil


# view d'accueil : OK
def index(request):
    request.session["page_active"]=1
    annonces = Annonce.objects.filter(etat = 2)
    return render(request, template_name="frontend/index.html", context={'annonces':  annonces})


# view de la page d'actualite
def actualite(request):
    request.session["page_active"]=1  # page d'actualite active
    articles = Article.objects.all()
    return render(request, template_name="frontend/actualite.html", context={'articles':  articles})


# page détails article
def article(request, pk=0):
    request.session["page_active"]=1  # page d'actualite active
    article = Article.objects.get(pk=pk)
    return render(request, template_name="frontend/article.html", context={'article':  article})


# commenter un article
def commenter(request, pk=0):
    if request.method == "POST":
        form = CommentaireForm(request.POST)
        article = Article.objects.get(pk=pk)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article = article
            instance.save()
            return redirect('article', pk=pk)
        else :
            pass
    else:
        form = CommentaireForm()
        return render(request, template_name="frontend/commentaire.html", context = {"form": form})


# page liste des annonces publiées
def liste_annonces(request):
    request.session["page_active"]=2
    annonces = Annonce.objects.filter(etat=2)
    reference = request.GET.get('reference', None)
    if reference:
        annonces = annonces.filter(reference=reference)
    date_creation = request.GET.get('date_creation', None)
    print(date_creation)
    print(annonces)
    if date_creation:
        annonces = annonces.filter(date_creation__date=date_creation)
    print(annonces)
    type_annonce = int(request.GET.get('type_annonce', 0))
    if int(type_annonce) > 0:
        annonces = annonces.filter(type_annonce=type_annonce)
    return render(request, template_name="frontend/liste_annonces.html", context={'annonces':  annonces})


def inscription(request):
    if request.method == "POST":
        return render(request, template_name="frontend/profil.html")
    else:
        form = EntrepriseForm()
        return render(request, template_name="frontend/inscription.html", context={"form": form})


def profil(request):
    if request.method == "POST":
        return render(request, template_name="frontend/profil.html")
    else:
        form = EntrepriseForm()
        return render(request, template_name="frontend/profil.html", context={"form": form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Message envoyé avec succès. Merci")
            request.session["page_active"]=1
            return redirect('front')
        else:
            messages.add_message(request, messages.ERROR, "Une erreur est survenue ! veuillez réessayer. ")
            request.session["page_active"]=4
            return render(request, template_name="frontend/contact.html", context = {'form': form})
    else:
        request.session["page_active"]=4
        return render(request, template_name="frontend/contact.html")



def annuaire(request):
    request.session["page_active"]=3
    entreprises = Entreprise.objects.all()
    return render(request, template_name="frontend/annuaire.html", context={'entreprises':  entreprises})


def user_annonces(request):
    if request.user.is_authenticated:
        annonces = request.user.profil.annonces.all()
        return render(request, template_name="frontend/mes_annonces.html", context={'annonces':  annonces})
    else:
        return redirect('b-login')


def nouvelle_annonce(request): 
    if request.user.is_authenticated:
        form = AnnonceForm()
        return render(request, template_name="frontend/nouvelle_annonce.html", context = {"form": form})
    else:
        return redirect('b-login')


def tdb(request):
    if request.user.is_authenticated:
        return render(request, template_name="frontend/tdb.html")
    else:
        return redirect('b-login')

    
def packs(request):
    if request.user.is_authenticated:
        return render(request, template_name="frontend/packs.html")
    else:
        return redirect('b-login')
"""
# view pour rediriger les requetes 404 vers la page d'accueil
def not_found_view(request):
    return redirect('front')

# view de la page d'accueil
def index(request):
    if request.user.is_authenticated :
        return redirect('b-agenda-tout')
    else:
        return redirect('b-login')

# view de la page de connexion des membres de la commission

    
# view de la page de deconnexion des membres de la commission
# TODO : eliminer la varible de session is_authenticated
def backlogout(request):
    #request.session['is_authenticated'] = False
    logout(request)
    return redirect('front')

# view qui renvoie l'agenda du centre
def agenda(request):
    if request.user.is_authenticated :
        user = request.user
        centre = request.user.membre.centre
        rdv = RDV.objects.filter(centre=centre).order_by('heure_rdv')
        return render(request, template_name="backend/agenda.html", context={'rdv': rdv})
    else:
        return redirect('b-login')


# TODO : ajout message success apres modification
def infos_beneficiaire(request, cin=None):
    if request.user.is_authenticated :
        regions = Region.objects.all()
        provinces = Province.objects.all()
        communes = Commune.objects.all()
        if not cin is None:
            try:
                beneficiaire = Beneficiaire.objects.get(cin=cin)
                rdv = RDV.objects.filter(beneficiaire=beneficiaire)              
                visites = Visite.objects.filter(beneficiaire=beneficiaire)
                demandes = Demande.objects.filter(beneficiaire = beneficiaire)
                if request.method == "POST":
                    form = BeneficiaireForm(request.POST, instance=beneficiaire)
                    if form.is_valid():
                        form.save()
                        visites = Visite.objects.filter( beneficiaire = beneficiaire )
                        context={"beneficiaire": beneficiaire, 'genres': SEXE_CHOIX, "visites": visites, "communes": communes}
                        #return render(request, template_name="backend/infos_beneficiaire.html", context=context)
                        messages.add_message(request, messages.SUCCESS, "تم التحديث بنجاح")
                        return redirect('b-beneficiaire-infos', cin=beneficiaire.cin)
                    else:
                        context = {
                            'beneficiaire': beneficiaire,
                            'form': form,
                            'error': True,
                            'genres': SEXE_CHOIX,
                            'regions': regions,
                            'provinces': provinces,
                            'communes': communes,
                            'rdv': rdv,
                            'visites': visites,
                            'demandes': demandes,
                        }
                        return render(request, template_name="backend/infos_beneficiaire.html", context=context)
                else:
                    success = False
                    if 'success' in request.GET:
                        success = True
                    
                    context = {
                        'beneficiaire': beneficiaire,
                        'genres': SEXE_CHOIX,
                        'visites': visites,
                        'rdv': rdv,
                        'demandes': demandes,
                        'success': success,
                        'regions': regions,
                        'provinces': provinces,
                        'communes': communes
                    }
                    return render(request, template_name="backend/infos_beneficiaire.html", context=context)
            except:
                return render(request, template_name="backend/recherche_beneficiaire.html", context={"error": True})
        else:
            request.session['success']=False
            if 'cin_ben' in request.GET:
                cin = request.GET['cin_ben']
                try:
                    beneficiaire = Beneficiaire.objects.get(cin=cin)
                    rdv = RDV.objects.filter(beneficiaire=beneficiaire)              
                    visites = Visite.objects.filter(beneficiaire=beneficiaire)
                    context = {
                        'beneficiaire': beneficiaire, 
                        'genres': SEXE_CHOIX,
                        'visites': visites,
                        'rdv': rdv,
                        'regions': regions,
                        'provinces': provinces,
                        'communes': communes, 
                    }
                    return render(request, template_name="backend/infos_beneficiaire.html", context=context)
                except:
                    return render(request, template_name="backend/recherches_beneficiaire.html", context={"error": True})
            else:
                return render(request, template_name="backend/recherche@_beneficiaire.html", context={"error": False})
    else:
        return redirect('b-login')

# view de recherche du bénéficiaire
def search_beneficiaire(request):
    if request.user.is_authenticated :
        if 'cin' in request.GET:
            cin = request.GET['cin']
            if Beneficiaire.objects.filter(cin__iexact=cin).exists():
                return redirect('b-beneficiaire-infos', cin=cin)
            else:
                # TODO : renvoyer vers la page d'ajout d'un nouveau beneficiaire au cas non trouve
                #return render(request, template_name="backend/recherche_beneficiaire.html", context={"error": True})
                messages.add_message(request, messages.ERROR, "لا يوجد مستفيد(ة) يحمل رقم البطاقة %s. يمكنك إضافة مستفيد (ة) من خلال تعبئة الاستمارة أدناه." %(cin))
                return redirect('b-beneficiaire-add')
        else:
            return render(request, template_name="backend/recherche_beneficiaire.html", context={"error": False})
    else:
        return redirect('b-login')


# view qui affiche le formulaire d'ajout d'un bénéficiaire
# TODO : ( VERIFIER L'EXISTENCE D'UN BENEF AVEC MEME CIN  ))
def add_beneficiaire(request):
    if request.user.is_authenticated :
        communes = Commune.objects.all()
        if request.method == "POST":
            form = BeneficiaireForm(request.POST)
            if form.is_valid():
                cin=form.cleaned_data['cin']
                cin_espace= str(form.cleaned_data['cin']).replace(" ", "")
                if Beneficiaire.objects.filter(cin__iexact=form.cleaned_data['cin']).exists() or Beneficiaire.objects.filter(cin__iexact=cin_espace).exists():
                    messages.add_message(request, messages.ERROR, "المستفيد(ة) الذي يحمل رقم البطاقة %s مسجل" %(form.cleaned_data['cin']))
                    return render(request, template_name="backend/nouveau_beneficiaire.html", context={'form': form, 'error': True, 'genres': SEXE_CHOIX, "communes": communes})
                beneficiaire = form.save(commit=False)
                beneficiaire.adresse_region = beneficiaire.adresse_commune.region
                beneficiaire.adresse_province = beneficiaire.adresse_commune.province
                beneficiaire.save()
                visites = Visite.objects.filter( beneficiaire = beneficiaire )
                context={"beneficiaire": beneficiaire, 'genres': SEXE_CHOIX, "visites": visites, "communes": communes}
                messages.add_message(request, messages.SUCCESS, "تم إضافة المستفيد(ة) بنجاح")
                return redirect('b-beneficiaire-infos', cin=beneficiaire.cin)
            else:
                return render(request, template_name="backend/nouveau_beneficiaire.html", context={'form': form, 'error': True, 'genres': SEXE_CHOIX, "communes": communes})
        elif request.method == "GET":
            form = BeneficiaireForm()
            return render(request, template_name="backend/nouveau_beneficiaire.html", context={'form': form, 'genres': SEXE_CHOIX, "communes": communes})
    else:
        return redirect('b-login')


# view qui affiche le formulaire d'ajout d'un bénéficiaire
# TODO : (A REVOIR)
def update_beneficiaire(request, cin):
    if request.user.is_authenticated :
        communes = Commune.objects.all()
        if request.method == "POST":
            beneficiaire = Beneficiaire.objects.get(cin = cin )
            form = BeneficiaireForm(request.POST, instance=beneficiaire)
            if form.is_valid():
                form.save()
                visites = Visite.objects.filter( beneficiaire = beneficiaire )
                context={"beneficiaire": beneficiaire, 'genres': SEXE_CHOIX, "visites": visites, "communes": communes}
                #return render(request, template_name="backend/infos_beneficiaire.html", context=context)
                return redirect('b-beneficiaire-infos', cin=beneficiaire.cin)
            else:
                return render(request, template_name="backend/infos_beneficiaire.html", context={'form': form, 'error': True, 'genres': SEXE_CHOIX, "communes": communes})
        elif request.method == "GET":
            form = BeneficiaireForm()
            return render(request, template_name="backend/nouveau_beneficiaire.html", context={'form': form, 'genres': SEXE_CHOIX, "communes": communes})
    else:
        return redirect('b-login')


# view qui affiche le formulaire d'ajout d'un bénéficiaire
# TODO : (A REVOIR)
from django_xhtml2pdf.utils import generate_pdf
from django.http import HttpResponse
def add_rdv(request):
    if request.user.is_authenticated :
        centres = Centre.objects.all()
        services = Prestation.objects.all()
        if request.method == "POST":
            form = RDVForm(request.POST) 
            if form.is_valid():
                centre = form.cleaned_data['centre']
                date_rdv = form.cleaned_data['date_rdv']
                heure_rdv = form.cleaned_data['heure_rdv']
                nature_rdv = form.cleaned_data['nature']
                if RDV.objects.filter(centre=centre, date_rdv=date_rdv, heure_rdv=heure_rdv).exists() and nature_rdv == 1:
                    messages.add_message(request, messages.ERROR, "الموعد الذي تم تحديده غير متاح, يرجى اختيار موعد آخر")
                    beneficiaires = Beneficiaire.objects.all()
                    context = {
                        'form': form,
                        'beneficiaires': beneficiaires,
                        'centres' : centres,
                        'services': services,
                        'etats': NATURE_RDV,
                        'heures': HEURE_RDV,
                    }
                    return render(request, template_name="backend/agenda_rdv.html", context=context)
                rdv = form.save()
                messages.add_message(request, messages.SUCCESS, "تمت برمجة موعد يوم %s على الساعة %s للمستفيد %s" %(rdv.date_rdv, rdv.get_heure_rdv_display(), rdv.beneficiaire))
                # TODO: GENERER FICHE D ORIENTATON > CODE RDV + INFOS BENEFICIAIRE + COORDONNÉES CENTRES
                return redirect('b-beneficiaire-infos', cin=rdv.beneficiaire.cin)
            else:
                beneficiaires = Beneficiaire.objects.all()
                context = {
                    'form': form,
                    'error': True,
                    'beneficiaires': beneficiaires,
                    'centres' : centres,
                    'services': services,
                    'etats': NATURE_RDV,
                    'heures': HEURE_RDV,
                }
                return render(request, template_name="backend/nouveau_rdv.html", context=context)
        elif request.method == "GET":
            form = RDVForm()
            beneficiaires = 0
            datalist = False
            if 'beneficiaire' in request.GET and request.GET['beneficiaire']:
                datalist = False
                beneficiaires = Beneficiaire.objects.filter(pk=request.GET['beneficiaire'])
            else:
                datalist = True
                beneficiaires = Beneficiaire.objects.all()
            context = {
                'form': form,
                'beneficiaires': beneficiaires,
                'centres' : centres,
                'services': services,
                'etats': NATURE_RDV,
                'heures': HEURE_RDV,
                'datalist': datalist,
            }
            return render(request, template_name="backend/agenda_rdv.html", context=context)
    else:
        return redirect('b-login')

from utils import render_to_pdf
def fiche_orientation(request, pk):
    #resp = HttpResponse(content_type='application/pdf')
    #result = generate_pdf('backend/fiche_orientation.html', file_object=resp)
    #return result
    rdv = RDV.objects.get(pk=pk)
    return render_to_pdf('backend/fiche_orientation.html', context_dict ={'rdv': rdv})

from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.conf import settings
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.utils import django_url_fetcher

class FicheOrientationView(TemplateView):

    template_name = "backend/fiche_orientation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rdv'] = RDV.objects.get(pk=kwargs.get('pk'))
        return context
class OrientationView(DetailView):
    # vanilla Django DetailView
    template_name = 'backend/fiche_orientation.html'

def custom_url_fetcher(url, *args, **kwargs):
    # rewrite requests for CDN URLs to file path in STATIC_ROOT to use local file
    cloud_storage_url = 'https://s3.amazonaws.com/django-weasyprint/static/'
    if url.startswith(cloud_storage_url):
        url = 'file://' + url.replace(cloud_storage_url, settings.STATIC_URL)
    return django_url_fetcher(url, *args, **kwargs)

class OrientationFicheView(WeasyTemplateResponseMixin, FicheOrientationView):
    # dynamically generate filename
    def get_pdf_filename(self):
        return 'orientation-.pdf'
    
def agenda_centre(request):
    # request.is_ajax() is deprecated since django 3.1
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if  is_ajax:
        if request.method == 'GET':
            centre_id = request.GET['centre']
            centre = Centre.objects.get(pk= centre_id)
            rdv = RDV.objects.filter(centre=centre).order_by('heure_rdv')
            prestations = Prestation.objects.filter(centre = centre)
            events = []
            for rd in rdv :
                event = {}
                event['id'] = rd.pk
                event['name'] = "%s (%s)" %(rd.prestation_demandee, rd.get_nature_display())
                event['description'] = "%s - %s" %(rd.beneficiaire.nom_complet_ar(), rd.beneficiaire.cin)
                event['year'] = rd.date_rdv.year
                event['month'] = rd.date_rdv.month
                event['day'] = rd.date_rdv.day
                event['etat'] = rd.get_nature_display()
                event['heure'] = rd.get_heure_rdv_display()
                events.append(event)
            rdv = list(events)
            services = []
            for service in prestations :
                prestation = {}
                prestation['id'] = service.pk
                prestation['nom'] = service.nom
                services.append(prestation)
            prestations = list(services)
            return JsonResponse({'rdv': events, 'prestations': prestations})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')
    

# view ajax qui renvoie si l'horaire choisi pour le rdv est dispo ou non
def agenda_heure(request):
    # request.is_ajax() is deprecated since django 3.1
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if  is_ajax:
        if request.method == 'GET':
            centre_id = request.GET['centre']
            heure_rdv = request.GET['heure_rdv']
            date_rdv = request.GET['date_rdv']
            centre = Centre.objects.get(pk= centre_id)
            disponible = True
            if RDV.objects.filter(centre=centre, date_rdv=date_rdv, heure_rdv=heure_rdv).exists():
                disponible = False
                return JsonResponse({'disponible': disponible,})
            else: 
                disponible = True
                return JsonResponse({'disponible': disponible,})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

# view d'ajout d'une visite
def add_visite(request):
    if request.user.is_authenticated :
        user = request.user.membre
        centre = user.centre
        if request.method == "POST":
            form = VisiteForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('b-list-visite-tout')
        else:
            services = Prestation.objects.filter(centre=centre)
            type_visite = NATURE_VISITE
            form = VisiteForm()
            context = {
                'form': form,
                'services': services,
                'type_visite': type_visite,
                'centre': centre,
                'heure_visite': HEURE_VISITE
            }
            if 'cin' in request.GET:
                cin = request.GET['cin']
                beneficiaire = Beneficiaire.objects.get(cin=cin)
                rdv = RDV.objects.filter(centre = centre, beneficiaire = beneficiaire)
                context['beneficiaire'] = beneficiaire
            else:
                beneficiaires = Beneficiaire.objects.all()
                rdv = RDV.objects.filter(centre=centre)
                context['beneficiaires'] = beneficiaires
            context['rdv'] = rdv
            return render(request, template_name="backend/nouveau_visite.html", context=context)
    else:
        return redirect('b-login')

# view qui renvoie la liste des visites programmees : choix n°2
def list_visites_programmees(request):
    if request.user.is_authenticated :
        rdv = RDV.objects.filter(etat=1)
        return render(request, template_name="backend/visites_programmees.html", context={'visites': visites})
    else:
        return redirect('b-login')
    
# view qui renvoie la liste globale des visites
def list_visites(request):
    if request.user.is_authenticated :
        centre = request.user.membre.centre
        visites = Visite.objects.filter(centre = centre)
        return render(request, template_name="backend/visites_liste.html", context={'visites': visites})
    else:
        return redirect('b-login')


# view qui renvoie la liste globale des visites
def list_demandes(request):
    if request.user.is_authenticated :
        centre = request.user.membre.centre
        demandes = Demande.objects.filter(centre = centre)
        return render(request, template_name="backend/demandes_liste.html", context={'demandes': demandes})
    else:
        return redirect('b-login')


# view d'ajout d'une demande
def add_demande(request):
    if request.user.is_authenticated :
        user = request.user.membre
        centre = user.centre
        if request.method == "POST":
            form = DemandeForm(request.POST)
            if form.is_valid():
                demande = form.save()
                return redirect('b-list-demandes-tout')
            else:
                services = Prestation.objects.filter(centre=centre)
                context = {
                    'form': form,
                    'services': services,
                    'etat_demande': ETAT_DEMANDE,
                    'appareils': APPAREILS,
                    'centre': centre,
                }
                return render(request, template_name="backend/nouveau_demande.html", context=context)
        else:
            services = Prestation.objects.filter(centre=centre)
            etat_demande = ETAT_DEMANDE
            form = DemandeForm()
            context = {
                'form': form,
                'services': services,
                'etat_demande': etat_demande,
                'appareils': APPAREILS,
                'centre': centre,
            }
            if 'cin' in request.GET:
                cin = request.GET['cin']
                beneficiaire = Beneficiaire.objects.get(cin=cin)
                visites = Visite.objects.filter(centre = centre, beneficiaire = beneficiaire)
                context['beneficiaire'] = beneficiaire
            else:
                beneficiaires = Beneficiaire.objects.all()
                visites = Visite.objects.filter(centre=centre)
                context['beneficiaires'] = beneficiaires
            context['visites'] = visites
            return render(request, template_name="backend/nouveau_demande.html", context=context)
    else:
        return redirect('b-login')

# view de mise à jour de demande
def update_demande(request, pk):
    if request.user.is_authenticated :
        communes = Commune.objects.all()
        if request.method == "POST":
            demande = Demande.objects.get(pk = pk )
            form = DemandeForm(request.POST, instance=demande)
            if form.is_valid():
                form.save()
                context = {}
                #return render(request, template_name="backend/infos_beneficiaire.html", context=context)
                messages.add_message(request, messages.SUCCESS, "تم تحديث الطلب رقم %s بنجاح " %(demande.slug()))
                return redirect('b-list-demandes-tout')
            else:
                context = {'form': form, 'demande': demande, 'error': True, 'etat_demande': ETAT_DEMANDE }
                return render(request, template_name="backend/update_demande.html", context = context)
        elif request.method == "GET":
            form = BeneficiaireForm()
            demande = Demande.objects.get(pk = pk )
            context = {
                'form': form,
                'etat_demande': ETAT_DEMANDE,
                "demande": demande,
            }
            return render(request, template_name="backend/update_demande.html", context = context)
    else:
        return redirect('b-login')

# view de la page espace perso de psh
# TODO : A REVOIR
def espace(request):
    return render(request, template_name="frontend/espace.html")


# view qui affiche la liste des coaph filtree par region/province
# TODO : ajout filtre commune
def centres(request):
    centres = Centre.objects.all()
    provinces = Province.objects.all()
    regions = Region.objects.all()
    province_selected = 0
    region_selected = 0
    try:
        region = int(request.GET['region'])
        if region != 0 :
            adresse_region = Region.objects.get(pk=region)
            centres=centres.filter(region=adresse_region)
            provinces = provinces.filter(region=adresse_region)
            region_selected = region
    except:
        pass
    try:
        province = int(request.GET['province'])
        if province != 0 :
            adresse_province = Province.objects.get(pk=province)
            centres=centres.filter(province=adresse_province)
            province_selected = province
    except:
        pass
    context = {
        "centres": centres, 
        "regions": regions, 
        "provinces": provinces, 
        "province_selected": province_selected, 
        "region_selected": region_selected,
        "types":TYPE_CENTRE
    }
    return render(request, template_name="frontend/centres.html", context=context)


# view qui affiche la page détail du coaph
def centre(request, pk=None):
    centre = Centre.objects.get(pk=pk)
    return render(request, template_name="frontend/centre_map.html", context={"centre": centre})
"""
