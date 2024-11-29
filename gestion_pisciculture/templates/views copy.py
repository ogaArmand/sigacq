from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import json
from django.shortcuts import render, redirect,get_object_or_404, HttpResponseRedirect
from datetime import date, timedelta, datetime
from django.contrib.humanize.templatetags.humanize import intcomma
from django import template
from django.db.models import Func
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
import string
import random
from django.urls import reverse
import hashlib
import hmac
import requests
from django.db.models import Count
# import pandas as pd
from django.db.models.functions import TruncMonth
# Create your views here.

# import matplotlib
# matplotlib.use('Agg')  # Utiliser le backend non interactif pour Matplotlib

from datetime import datetime
# from matplotlib.dates import MonthLocator, DateFormatter
# import pandas as pd
# import matplotlib.pyplot as plt
from django.http import HttpResponse
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum, Avg
from django.utils import timezone

from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import urllib, base64
import matplotlib.ticker as ticker
from django.utils.timezone import now
from decimal import Decimal

from twilio.rest import Client
from django.conf import settings


groupe = None


def open_admin(request):
    return redirect('/admin/')

def moisenlettre():
    mois_en_lettres = {
    1: 'Janvier',
    2: 'Février',
    3: 'Mars',
    4: 'Avril',
    5: 'Mai',
    6: 'Juin',
    7: 'Juillet',
    8: 'Août',
    9: 'Septembre',
    10: 'Octobre',
    11: 'Novembre',
    12: 'Décembre'
    }

# Obtenez le mois actuel
    mois_en_cours = datetime.now().month

# Convertissez le numéro du mois en lettre en utilisant le dictionnaire
    mois_en_lettres = mois_en_lettres[mois_en_cours]
    return mois_en_lettres


class Unaccent(Func):
    function = 'UNACCENT'

register = template.Library()

@register.filter(name='intspace')
def intspace(value):
    """
    Similar to intcomma, but uses spaces as thousand separators instead of commas.
    """
    orig_value = intcomma(value)
    return orig_value.replace(',', ' ')

def loginuser(request):
    return render(request,'login.html')


@csrf_exempt
def connexion(request):
    username = request.POST.get('username')
    password = request.POST.get('pass')
    # Authentifier l'utilisateur avec les informations d'identification fournies
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Connecter l'utilisateur s'il est authentifié avec succès
        login(request, user)
        request.session['user_connecte'] = 1
        request.session['user_id'] = user.id
        request.session['user_name'] = user.last_name
        request.session['user_prenom'] = user.first_name
        request.session['user_login'] = user.username
        request.session['email'] = user.email

        
        return JsonResponse({'status': 'ok'})
    else:
        print('user non connecté')
        return JsonResponse({'status': 'PasOk'})

def seuil_depense(total_depenses):
    config = Configuration.objects.first()
    if not config:
        return  # Si aucune configuration n'existe, ne rien faire

    seuil = config.seuil_depense
    # Vérifier si le seuil est atteint ou dépassé
    if total_depenses >= seuil:
        return True
    else :
        return False


def accueil(request):
    user_connecte = request.session.get('user_connecte', None)
    user_cf = request.session.get('user_cf', None)
    aujourdhui = date.today()
    if user_connecte is None:
        # La variable de session user_cf n'existe pas, rediriger vers la page de connexion
        return redirect('loginuser')
    # Dépenses pour l'alimentation
    cout_alimentation = Depense.objects.filter(categorie='alimentation').aggregate(total_cost=Sum('montant'))['total_cost'] or 0
    
    # Dépenses pour les soins
    cout_soins = Depense.objects.filter(categorie='soin').aggregate(total_cost=Sum('montant'))['total_cost'] or 0

    # Dépenses pour l'infrastructure
    cout_infrastructure = Depense.objects.filter(categorie='infrastructure').aggregate(total_cost=Sum('montant'))['total_cost'] or 0

    # Dépenses pour autres catégories
    cout_autre = Depense.objects.filter(categorie='autre').aggregate(total_cost=Sum('montant'))['total_cost'] or 0

    couts_production = cout_alimentation + cout_soins + cout_autre

    couts_vente = Vente.objects.aggregate(total_cost=Sum('prix_vente'))['total_cost'] or 0
    # Calcul du prix moyen de vente
    prix_moyen_vente = LigneCommande.objects.aggregate(avg_prix_vente=Avg('prix_unitaire'))['avg_prix_vente'] or 0
    
    quantite_vendu = LigneCommande.objects.aggregate(total_cost=Sum('quantite'))['total_cost'] or 0

    poids_vendu = LigneCommande.objects.aggregate(total_cost=Sum('poids'))['total_cost'] or 0

    quantite_dispo = Poisson.objects.aggregate(total_cost=Sum('nombre_poisson_dispo'))['total_cost'] or 0
    nombre_alevins = Poisson.objects.aggregate(total_cost=Sum('nombre_alevins'))['total_cost'] or 0

    taux_mortalite = 10

    duree = 180

    benefice = couts_vente-couts_production

    # Récupérer les ventes et dépenses de l'année en cours
    annee_actuelle = date.today().year
    
    ventes = (
        Vente.objects.filter(date_vente__year=annee_actuelle)
        .annotate(mois=TruncMonth('date_vente'))
        .values('mois')
        .annotate(total=Sum('prix_vente'))
        .order_by('mois')
    )
    depenses = (
        Depense.objects.filter(date_depense__year=annee_actuelle)  # Filtrer par année en cours
        .exclude(categorie='infrastructure')  # Exclure la catégorie 'infrastructure'
        .annotate(mois=TruncMonth('date_depense'))  # Truncater pour obtenir le mois
        .values('mois')  # Sélectionner uniquement les mois
        .annotate(total=Sum('montant'))  # Calculer le total des montants par mois
        .order_by('mois')  # Trier par mois
    )

    # Rassembler les mois et les données dans des dictionnaires
    data_ventes = {entry['mois']: entry['total'] for entry in ventes}
    data_depenses = {entry['mois']: entry['total'] for entry in depenses}
    
    # Obtenir tous les mois de l'année en cours
    mois_labels = sorted(set(data_ventes.keys()).union(data_depenses.keys()))

    # Extraire les montants de ventes, dépenses et bénéfices par mois
    montant_ventes = [data_ventes.get(mois, 0) for mois in mois_labels]
    montant_depenses = [data_depenses.get(mois, 0) for mois in mois_labels]
    montant_benefices = [v - d for v, d in zip(montant_ventes, montant_depenses)]

    # Créer des libellés de mois au format "Jan", "Feb", etc.
    mois_labels_str = [mois.strftime('%b') for mois in mois_labels]

    # Création du graphique en courbes
    plt.figure(figsize=(9, 4))
    plt.plot(mois_labels_str, montant_ventes, label="Ventes", color="#4e73df", marker="o")
    plt.plot(mois_labels_str, montant_depenses, label="Dépenses", color="orange", marker="o")
    plt.plot(mois_labels_str, montant_benefices, label="Bénéfices", color="#1cc88a", marker="o")

        # Obtenir le seuil actuel de la configuration
    config = Configuration.objects.first()
    if not config:
        return  # Si aucune configuration n'existe, ne rien faire

    seuil = config.seuil_depense
        # Ajouter une ligne de repère sur y=0 pour distinguer les valeurs positives et négatives
  # Ajouter une ligne horizontale
    plt.axhline(seuil, color='red', linewidth=2, label="Seuil de dépense mensuel")

    # Ajouter les montants au-dessus de chaque point pour Ventes, Dépenses, et Bénéfices
    for i, mois in enumerate(mois_labels_str):
        plt.text(mois, montant_ventes[i], intspace(f"{montant_ventes[i]:,.0f}"), ha='center', va='bottom', fontsize=8, color="#4e73df")
        plt.text(mois, montant_depenses[i], intspace(f"{montant_depenses[i]:,.0f}"), ha='center', va='bottom', fontsize=8, color="orange")
        plt.text(mois, montant_benefices[i], intspace(f"{montant_benefices[i]:,.0f}"), ha='center', va='bottom', fontsize=8, color="#1cc88a")
    
        # Formater l'axe des y pour afficher les montants avec des séparateurs de milliers
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: intspace(f"{int(x):,}")))


    plt.xlabel('Mois')
    plt.ylabel('Montant (FCFA)')
    # plt.title('Montants des Ventes, Dépenses et Bénéfices par Mois (Année en cours)')
    plt.xticks(rotation=45)
    plt.tight_layout()  # Ajustement automatique pour que tout soit visible
    plt.legend()

    # Convertir le graphique en image pour l'inclure dans le template HTML
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    graphique_base64 = base64.b64encode(image_png)
    graphique_url = 'data:image/png;base64,{}'.format(graphique_base64.decode())
    buf.close()

   
    # investissement_total = cout_infrastructure -benefice # Investissement total (ex: 1 million FCFA)
    # bénéfice = benefice  # Bénéfice net réalisé (ex: 300 000 FCFA)

        # Calcul des tailles pour le graphique circulaire
    bénéfice = max(benefice, 0)  # Assurez-vous que bénéfice soit non négatif
    investissement_total = max(cout_infrastructure - bénéfice, 0)

    # Labels pour le graphique
    labels = ['Reste à amortir', 'amortissement réalisé']
    # Données à afficher (total investissement, amortissement, bénéfice)
    sizes = [investissement_total, bénéfice]

    # Couleurs des sections du camembert
    colors = ['#ff9999', '#99ff99']

    # Fonction pour afficher à la fois le montant et le pourcentage
    def autopct_with_amount(pct, values):
        total = sum(values)
        absolute = round(pct / 100 * float(total))  # Convertir total en float pour éviter l'erreur
        absolute_formatted = intspace("{:,.0f}".format(absolute))  # Format avec séparateur de milliers
        return f'{absolute_formatted} FCFA\n({pct:.1f}%)'

    # Création du graphique en camembert
    plt.figure(figsize=(4, 4))  # Taille du graphique
    plt.pie(sizes, colors=colors, autopct=lambda pct: autopct_with_amount(pct, sizes), startangle=90)

    # Ajouter une légende en dessous du camembert
    plt.legend(labels, loc="center", fontsize=10, bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False)


    # Ajouter un titre
    # plt.title('')

    plt.tight_layout()
    # Sauvegarder l'image dans un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convertir l'image en base64
    image_png = buf.getvalue()
    graphique_base64 = base64.b64encode(image_png)
    graphique_url_camembert = 'data:image/png;base64,{}'.format(graphique_base64.decode())

    # Fermer le buffer
    buf.close()

    # Retourner l'URL base64 pour affichage dans le template


    # Obtenir l'année en cours
    annee_courante = now().year

    # Calculer le total des dépenses pour l'année en cours
    total_depenses = Depense.objects.filter(date_depense__year=annee_courante).exclude(categorie='infrastructure').aggregate(total=Sum('montant'))['total'] or 0

    # Calculer le total des ventes pour l'année en cours
    total_ventes = Vente.objects.filter(date_vente__year=annee_courante).aggregate(total=Sum('prix_vente'))['total'] or 0

    # Calculer le bénéfice annuel
    # Supposons que le bénéfice = total_ventes - total_depenses
    total_benefice = total_ventes - total_depenses

    montant_depenses_dispo = seuil-total_depenses
    
    if seuil == 0:
        taux_seuil = 0  # Ou toute autre valeur par défaut pertinente
        taux_total_depenses = 0  # On ne peut pas calculer un pourcentage si le seuil est 0
    else:
        taux_seuil = 100  # Toujours 100, car seuil/seuil = 1
        taux_total_depenses = round((total_depenses / seuil) * 100)
        taux_dispo = round((montant_depenses_dispo / seuil) * 100)

    # Calcul des totaux des dépenses (hors infrastructure) par année
    depenses_par_annee = (
        Depense.objects
        .exclude(categorie='infrastructure')
        .values('date_depense__year')
        .annotate(total_depenses=Sum('montant'))
    )
    
    # Calcul des totaux des ventes par année
    ventes_par_annee = (
        Vente.objects
        .values('date_vente__year')
        .annotate(total_ventes=Sum('prix_vente'))
    )
    
    # Calcul du total des alevins introduits par année
    poissons_par_annee = (
        Poisson.objects
        .values('date_introduction__year')
        .annotate(total_poissons=Sum('nombre_alevins'))
    )
    
    # Initialisation du dictionnaire pour stocker les données par année
    tableau = {}

    # Intégration des dépenses
# Supposons que `seuil` est défini comme suit :

    # Intégration des dépenses dans le tableau
    for depense in depenses_par_annee:
        annee = depense['date_depense__year']
        
        # Initialisation de l'année si elle n'existe pas encore dans le tableau
        if annee not in tableau:
            tableau[annee] = {
                'total_depenses': depense['total_depenses'],
                'total_ventes': 0,
                'total_benefice': 0,
                'total_poissons': 0
            }
        else:
            # Mise à jour des dépenses pour l'année si déjà présente
            tableau[annee]['total_depenses'] += depense['total_depenses']
        
        # Classification de la dépense selon le seuil
        if depense['total_depenses'] <= seuil * Decimal('0.5'):
            tableau[annee]["depense_class"] = "text-success"  # Dépenses faibles (bonnes)
        elif depense['total_depenses'] <= seuil * Decimal('0.7'):
            tableau[annee]["depense_class"] = "text-warning"  # Dépenses modérées
        else:
            tableau[annee]["depense_class"] = "text-danger"  # Dépenses élevées



    # Intégration des ventes
    for vente in ventes_par_annee:
        annee = vente['date_vente__year']
        if annee in tableau:
            tableau[annee]['total_ventes'] = vente['total_ventes']
        else:
            tableau[annee] = {
                'total_depenses': 0,
                'total_ventes': vente['total_ventes'],
                'total_benefice': 0,
                'total_poissons': 0
            }

    # Intégration des poissons
    for poisson in poissons_par_annee:
        annee = poisson['date_introduction__year']
        if annee in tableau:
            tableau[annee]['total_poissons'] = poisson['total_poissons']
        else:
            tableau[annee] = {
                'total_depenses': 0,
                'total_ventes': 0,
                'total_benefice': 0,
                'total_poissons': poisson['total_poissons']
            }

    # Calcul des bénéfices pour chaque année
    for annee, data in tableau.items():
        data['total_benefice'] = data['total_ventes'] - data['total_depenses']

    print(tableau)
    # Passer les données au template

    context = {
        'taux_dispo':taux_dispo,
        'taux_seuil':taux_seuil,
        'taux_total_depenses':taux_total_depenses,
        'tableau': tableau,
        'seuil':seuil,
        'montant_depenses_dispo':montant_depenses_dispo,
        'total_depenses': total_depenses,
        'total_ventes': total_ventes,
        'total_benefice': total_benefice,
        'annee_courante': annee_courante,
        'graphique_url':graphique_url,
        'graphique_url_camembert':graphique_url_camembert,
        'couts_production':couts_production,
        'couts_vente':couts_vente,
        'benefice':benefice,
        'prix_moyen_vente':prix_moyen_vente,
        'cout_infrastructure':cout_infrastructure,
        'quantite_vendu':quantite_vendu,
        'poids_vendu':poids_vendu,
        'taux_mortalite':taux_mortalite,
        'duree_elevage':duree,
        'quantite_dispo':quantite_dispo,
        'nombre_alevins':nombre_alevins,
    }

# tables.html
    return render(request,'index.html',context)

def create_account(request):
    return render(request,'create_account.html')

def calculer_rentabilite():
    total_ventes = Vente.objects.aggregate(Sum('prix_vente'))['prix_vente__sum'] or 0
    total_depenses = Depense.objects.aggregate(Sum('montant'))['montant__sum'] or 0
    return total_ventes - total_depenses


def calculer_nombre_alevins(bénéfice_cible, prix_vente_kg, taux_mortalite, poids_final_moyen_kg):
    # Calcul du nombre de poissons nécessaires pour atteindre le bénéfice après mortalité
    nombre_poissons_a_vendre = bénéfice_cible / prix_vente_kg
    # Ajuster pour la mortalité
    nombre_alevins = nombre_poissons_a_vendre / (1 - taux_mortalite)
    return round(nombre_alevins)

def calculer_quantite_aliment(nombre_alevins, duree_elevage, taux_conversion, poids_final_moyen_kg):
    # Quantité totale d'aliment nécessaire pour l'élevage (approximatif)
    quantité_totale_aliment = nombre_alevins * poids_final_moyen_kg * taux_conversion
    return quantité_totale_aliment

def calculer_depenses(nombre_alevins, prix_alevin, quantité_aliment, prix_aliment_kg, autres_depenses):
    # Coût des alevins
    cout_alevins = nombre_alevins * prix_alevin
    # Coût de l'aliment
    cout_aliment = quantité_aliment * prix_aliment_kg
    # Dépenses totales
    depenses_totales = cout_alevins + cout_aliment + autres_depenses
    return depenses_totales


def prevision_production(bénéfice_cible, prix_vente_kg, taux_mortalite, poids_final_moyen_kg, duree_elevage, taux_conversion, prix_alevin, prix_aliment_kg, autres_depenses):
    # Calculer le nombre d'alevins
    nombre_alevins = calculer_nombre_alevins(bénéfice_cible, prix_vente_kg, taux_mortalite, poids_final_moyen_kg)
    
    # Calculer la quantité d'aliment nécessaire
    quantité_aliment = calculer_quantite_aliment(nombre_alevins, duree_elevage, taux_conversion, poids_final_moyen_kg)
    
    # Calculer les dépenses totales
    depenses = calculer_depenses(nombre_alevins, prix_alevin, quantité_aliment, prix_aliment_kg, autres_depenses)
    
    # Calculer le bénéfice net attendu
    ventes = nombre_alevins * (1 - taux_mortalite) * poids_final_moyen_kg * prix_vente_kg
    bénéfice_net = ventes - depenses
    
    return {
        "nombre_alevins": nombre_alevins,
        "quantité_aliment": quantité_aliment,
        "dépenses_totales": depenses,
        "bénéfice_net_attendu": bénéfice_net
    }


def bassin(request):
    if request.method == 'POST':
        form = BassinForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_bassins')  # Redirection vers la liste des poissons
    else:
        form = BassinForm()
    # Si la requête est GET, afficher le formulaire
    return render(request, 'bassin_ajout.html',{'form': form})


def liste_bassins(request):
    bassins = Bassin.objects.all()
    return render(request, 'bassins_liste.html', {'bassins': bassins})

def supprimer_bassin(request, id):
    bassin = get_object_or_404(Bassin, id=id)
    bassin.delete()
    return redirect('liste_bassins')  # Rediriger vers la liste des bassins après la suppression


def modifier_bassin(request):
    id = request.GET.get('id')
    bassin = get_object_or_404(Bassin, id=id)
    if request.method == 'POST':
        form = BassinForm(request.POST, instance=bassin)
        if form.is_valid():
            form.save()
            return redirect('liste_bassins')  # Redirection après modification
    else:
        form = BassinForm(instance=bassin)
    return render(request, 'bassin_modifier.html', {'form': form, 'bassin': bassin})

def ajouter_bande(request):
    if request.method == 'POST':
        form = BandeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_bande')  # Redirection vers la liste des poissons
    else:
        form = BandeForm()
    # Si la requête est GET, afficher le formulaire
    return render(request, 'bande_ajout.html',{'form': form})


def liste_bande(request):
    bandes = Bande.objects.all()
    return render(request, 'bande_liste.html', {'bandes': bandes})

def supprimer_bande(request, id):
    bande = get_object_or_404(Bande, id=id)
    bande.delete()
    return redirect('liste_bande')  # Rediriger vers la liste des bassins après la suppression


def modifier_bande(request):
    id = request.GET.get('id')
    bande = get_object_or_404(Bande, id=id)
    if request.method == 'POST':
        form = BandeForm(request.POST, instance=bande)
        if form.is_valid():
            form.save()
            return redirect('liste_bande')  # Redirection après modification
    else:
        form = BandeForm(instance=bande)
    return render(request, 'bande_modifier.html', {'form': form, 'bande': bande})


def Ajoutespece(request):
    if request.method == 'POST':
        form = especeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_espece')  # Redirection vers la liste des poissons
    else:
        form = especeForm()
    # Si la requête est GET, afficher le formulaire
    return render(request, 'espece_ajout.html',{'form': form})


def liste_espece(request):
    especepoissons = EspecePoisson.objects.all()
    return render(request, 'espece_liste.html', {'especepoissons': especepoissons})

def supprimer_espece(request, id):
    especePoisson = get_object_or_404(EspecePoisson, id=id)
    especePoisson.delete()
    return redirect('liste_espece')  # Rediriger vers la liste des bassins après la suppression

def modifier_espece(request):
    id = request.GET.get('id')
    especepoisson = get_object_or_404(EspecePoisson, id=id)

    if request.method == 'POST':
        form = especeForm(request.POST, instance=especepoisson)
        if form.is_valid():
            form.save()
            return redirect('liste_espece')  # Redirection après modification
    else:
        form = especeForm(instance=especepoisson)
    return render(request, 'espece_modifier.html', {'form': form, 'especepoisson': especepoisson})



def ajouter_poisson(request):
    if request.method == 'POST':
        form = PoissonForm(request.POST)
        if form.is_valid():
            form.save()
            # Mise à jour des stocks de poissons et de la bande associée
       
            return redirect('liste_poisson')  # Redirection vers la liste des poissons
    else:
        form = PoissonForm()
    return render(request, 'poisson_ajout.html', {'form': form})


def liste_poisson(request):
    poissons = Poisson.objects.all()
    return render(request, 'poisson_liste.html', {'poissons': poissons})

def modifier_poisson(request):
    id = request.GET.get('id')
    poisson = get_object_or_404(Poisson, id=id)
    if request.method == 'POST':
        form = PoissonForm(request.POST, instance=poisson)
        if form.is_valid():
            form.save()
            poisson.update_stock()
            return redirect('liste_poisson')  # Redirection après modification
    else:
        form = PoissonForm(instance=poisson)
    return render(request, 'poisson_modifier.html', {'form': form, 'poisson': poisson})


def supprimer_poisson(request):
    poisson_id = request.Get.get('id')
    poisson = get_object_or_404(Poisson, id=poisson_id)
    if request.method == 'POST':
        poisson.delete()
        return redirect('liste_poisson')  # Redirection après suppression


def ajouter_mortalite(request):
    if request.method == 'POST':
        form = MortaliteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_mortalite')  # Redirection vers la liste des poissons
    else:
        form = MortaliteForm()
    return render(request, 'mortalite_ajout.html', {'form': form})


def liste_mortalite(request):
    mortalites = Mortalite.objects.all()
    return render(request, 'mortalite_liste.html', {'mortalites': mortalites})

def modifier_mortalite(request):
    id = request.GET.get('id')
    mortalite = get_object_or_404(Mortalite, id=id)
    if request.method == 'POST':
        form = MortaliteForm(request.POST, instance=mortalite)
        if form.is_valid():
            form.save()
            return redirect('liste_mortalite')  # Redirection après modification
    else:
        form = MortaliteForm(instance=mortalite)
    return render(request, 'mortalite_modifier.html', {'form': form, 'poisson': mortalite})


def supprimer_mortalite(request):
    mortalite_id = request.Get.get('id')
    mortalite = get_object_or_404(Mortalite, id=mortalite_id)
    if request.method == 'POST':
        mortalite.delete()
        return redirect('liste_mortalite')  # Redirection après suppression


def ajouter_nourrirpoisson(request):
    if request.method == 'POST':
        form = NourrirpoissonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_nourrirpoisson')  # Redirection vers la liste des poissons
    else:
        form = NourrirpoissonForm()
    return render(request, 'nourrirpoisson_ajout.html', {'form': form})


def get_etapes_actives(request):
    poisson_id = request.GET.get('poisson_id')
    if poisson_id:
        etapes = EtapeEvolution.objects.filter(poisson_id=poisson_id, etat=True)
        etapes_data = [{'id': etape.id, 'name': str(etape)} for etape in etapes]
        return JsonResponse({'etapes': etapes_data})
    return JsonResponse({'etapes': []})

def liste_nourrirpoisson(request):
    nourrirpoissons = Nourrirpoisson.objects.all()
    return render(request, 'nourrirpoisson_liste.html', {'nourrirpoissons': nourrirpoissons})

def modifier_nourrirpoisson(request):
    id = request.GET.get('id')
    nourrirpoisson = get_object_or_404(Nourrirpoisson, id=id)
    if request.method == 'POST':
        form = NourrirpoissonForm(request.POST, instance=nourrirpoisson)
        if form.is_valid():
            form.save()
            return redirect('liste_nourrirpoisson')  # Redirection après modification
    else:
        form = NourrirpoissonForm(instance=nourrirpoisson)
    return render(request, 'nourrirpoisson_modifier.html', {'form': form, 'nourrirpoisson': nourrirpoisson})


def supprimer_nourrirpoisson(request):
    id = request.Get.get('id')
    nourrirpoisson = get_object_or_404(Nourrirpoisson, id=id)
    if request.method == 'POST':
        nourrirpoisson.delete()
        return redirect('liste_nourrirpoisson')  # Redirection après suppression


def Ajout_aliment(request):
    if request.method == 'POST':
        form = AlimentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_aliment')  # Redirection vers la liste des poissons
    else:
        form = AlimentForm()
        # Rediriger vers une autre page après l'enregistrement (par exemple une liste des bassins)
    return render(request, 'aliment_ajout.html', {'form': form})


def liste_aliment(request):
    aliments = Aliment.objects.all()
    return render(request, 'aliment_liste.html', {'aliments': aliments})

def supprimer_aliment(request, id):
    aliment = get_object_or_404(Aliment, id=id)
    aliment.delete()
    return redirect('liste_aliment')  # Rediriger vers la liste des bassins après la suppression

def modifier_aliment(request):
    id = request.GET.get('id')
    aliment = get_object_or_404(Aliment, id=id)

    if request.method == 'POST':
        form = AlimentForm(request.POST, instance=aliment)
        if form.is_valid():
            form.save()
            return redirect('liste_aliment')  # Redirection après modification
    else:
        form = AlimentForm(instance=aliment)
    return render(request, 'aliment_modifier.html', {'form':form,'aliment': aliment})


def distribuer_ration(request, poisson_id):
    poisson = get_object_or_404(Poisson, id=poisson_id)
    
    etape_actuelle = EtapeEvolution.objects.filter(poisson=poisson,etat=1).order_by('-date_debut').first()
   
    if etape_actuelle:
        aliments_recommandes = AlimentRecommande.objects.filter(espece=poisson.espece, stade=etape_actuelle.stade_actuel)
        i=0
        for aliment_rec in aliments_recommandes:
            
            # Calculer la quantité totale d'aliment à distribuer (nombre d'alevins * quantité recommandée par poisson)
            quantite_totale = poisson.nombre_poisson_dispo * aliment_rec.quantite_recommandee

            # Calculer le coût total pour ce type d'aliment
            cout_total = aliment_rec.calculer_cout_total(poisson.nombre_poisson_dispo)

            rationalimentaire_id = request.POST.get('id')
            # Vérifier s'il existe déjà une ration alimentaire pour ce poisson, aliment et date donnée
          
            try:
                ration_existante = RationAlimentaire.objects.get(id=rationalimentaire_id)
                # Mettre à jour les champs de la ration existante
                ration_existante.quantite = quantite_totale
                ration_existante.cout_total = cout_total
                ration_existante.save()
            except RationAlimentaire.DoesNotExist:
                # Créer une nouvelle ration si elle n'existe pas
                RationAlimentaire.objects.create(
                    poisson=poisson,
                    aliment=aliment_rec.aliment,
                    quantite=quantite_totale,
                    cout_total=cout_total,
                    date_distrib=timezone.now()
                )

        
        # Rediriger après distribution
        return redirect('liste_RationAlimentaire')
    else:
        # Gérer le cas où aucune étape n'est trouvée pour le poisson
        return HttpResponse("Aucune étape d'évolution trouvée pour ce poisson.")


def mettre_a_jour_ration_alimentaire():
    """
    Met à jour la ration alimentaire en fonction de l'étape actuelle du poisson.
    """
    poissons = Poisson.objects.all()

    for poisson in poissons:
        # Récupérer l'étape actuelle du poisson
        etape_actuelle = EtapeEvolution.objects.filter(poisson=poisson, etat=True).last()  # Assurez-vous d'avoir l'étape active

        if etape_actuelle:
            # Récupérer les aliments recommandés pour l'espèce du poisson et l'étape actuelle
            aliments_recommandes = AlimentRecommande.objects.filter(espece=poisson.espece, stade=etape_actuelle.stade_actuel)
            
            if aliments_recommandes.exists():
                # Mettre à jour la ration alimentaire de ce poisson avec les aliments recommandés
                for aliment_recommande in aliments_recommandes:
                    ration, created = RationAlimentaire.objects.update_or_create(
                        poisson=poisson,
                        defaults={
                            'quantite': aliment_recommande.quantite_recommandee*poisson.nombre_poisson_dispo,  # Quantité d'aliment recommandée pour ce poisson et ce stade
                            'cout_total': aliment_recommande.prix*poisson.nombre_poisson_dispo,  # Aliment spécifique recommandé
                            'aliment': aliment_recommande.aliment,  # Aliment spécifique recommandé
                        }
                    )
                    if created:
                        print(f"Ration alimentaire créée pour le poisson {poisson} au stade {etape_actuelle.stade_actuel}.")
                    else:
                        print(f"Ration alimentaire mise à jour pour le poisson {poisson} au stade {etape_actuelle.stade_actuel}.")
            else:
                print(f"Aucun aliment recommandé trouvé pour le poisson {poisson} au stade {etape_actuelle.stade_actuel}.")
        else:
            print(f"Aucune étape active trouvée pour le poisson {poisson}.")

from datetime import date, timedelta
from django.db.models import Q

def generer_suivi_automatique():
    """
    Génère automatiquement un SuiviAlimentaire pour chaque poisson en fonction de la date_debut de l'étape en cours,
    et crée un suivi pour chaque jour manquant depuis cette date_debut.
    """
    poissons = Poisson.objects.all()
    today = date.today()

    for poisson in poissons:
        try:
            # Vérifier si le poisson a une étape en cours (etat=True)
            etape = EtapeEvolution.objects.filter(poisson=poisson, etat=True).first()

            if etape:  # Si le poisson a une étape en cours
                start_date = etape.date_debut  # Utiliser la date_debut de l'étape comme point de départ
                delta = today - start_date

                # Générer un suivi pour chaque jour manquant depuis la date_debut de l'étape
                for i in range(delta.days + 1):
                    current_day = start_date + timedelta(days=i)

                    # Vérifier si un suivi existe déjà pour ce jour-là
                    if not SuiviAlimentaire.objects.filter(poisson=poisson, etapeevolution=etape, date_alimentation_auto=current_day).exists():
                        # Obtenir la ration alimentaire recommandée pour le poisson
                        ration_recom = RationAlimentaire.objects.get(poisson=poisson)

                        # Créer une nouvelle entrée de suivi alimentaire
                        SuiviAlimentaire.objects.create(
                            poisson=poisson,
                            etapeevolution=etape,
                            rationalimentaire_recom=ration_recom.quantite,  # Ration recommandée
                            rationalimentaire_donnee=0.0,  # Par défaut, aucune alimentation donnée
                            rationalimentaire_ecart=ration_recom.quantite,  # L'écart est total
                            date_alimentation_auto=current_day,  # Ajouter la date d'alimentation
                        )
                        print(f"Suivi alimentaire créé pour le poisson {poisson} pour la date {current_day}.")
                    else:
                        print(f"Suivi alimentaire déjà existant pour le poisson {poisson} à la date {current_day}.")
            else:
                print(f"Aucune étape en cours pour le poisson {poisson}.")
        except RationAlimentaire.DoesNotExist:
            print(f"Aucune ration alimentaire trouvée pour le poisson {poisson}.")


mettre_a_jour_ration_alimentaire()
generer_suivi_automatique()



def ajouter_RationAlimentaire(request):
    if request.method == 'POST':
        form = rationalimentaireForm(request.POST)
        if form.is_valid():
            poisson = form.cleaned_data['poisson']
            return distribuer_ration(request, poisson.id)  # Appeler distribuer_ration avec l'ID du poisson sélectionné
    else:
        form = rationalimentaireForm()

    return render(request, 'rationalimentaire_ajout.html', {'form': form})


def liste_RationAlimentaire(request):
    rationalimentaires = RationAlimentaire.objects.all()
    return render(request, 'rationalimentaire_liste.html', {'rationalimentaires': rationalimentaires})

def modifier_RationAlimentaire(request):
    id = request.GET.get('id')
    rationalimentaire = get_object_or_404(RationAlimentaire, id=id)
    if request.method == 'POST':
        form = rationalimentaireForm(request.POST, instance=rationalimentaire)
        if form.is_valid():
            poisson = form.cleaned_data['poisson']
            return distribuer_ration(request, poisson.id)  # Appeler distribuer_ration avec l'ID du poisson sélectionné
            # return redirect('liste_RationAlimentaire')  # Redirection après modification
    else:
        form = rationalimentaireForm(instance=rationalimentaire)
    return render(request, 'rationalimentaire_modifier.html', {'form': form, 'rationalimentaire': rationalimentaire})

def supprimer_RationAlimentaire(request):
    if request.method == 'POST':
        poisson_id = request.POST.get('id')
        rationalimentaire = get_object_or_404(RationAlimentaire, id=poisson_id)
        rationalimentaire.delete()
        return redirect('liste_RationAlimentaire')  # Redirection après suppression



def ajouter_EtapeEvolution(request):
    if request.method == 'POST':
        form = EtapeEvolutionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_EtapeEvolution')  # Redirection vers la liste des poissons
    else:
        form = EtapeEvolutionForm()
    return render(request, 'etapeevolution_ajout.html', {'form': form})


def liste_EtapeEvolution(request):
    etapeevolutions = EtapeEvolution.objects.filter(etat=True)
    return render(request, 'etapeevolution_liste.html', {'etapeevolutions': etapeevolutions})

def modifier_EtapeEvolution(request):
    id = request.GET.get('id')
    etapeevolution = get_object_or_404(EtapeEvolution, id=id)
    if request.method == 'POST':
        form = EtapeEvolutionForm(request.POST, instance=etapeevolution)
        if form.is_valid():
            form.save()
            return redirect('liste_EtapeEvolution')  # Redirection après modification
    else:
        form = EtapeEvolutionForm(instance=etapeevolution)
    return render(request, 'etapeevolution_modifier.html', {'form': form, 'etapeevolution': etapeevolution})


def supprimer_EtapeEvolution(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        etapeevolution = get_object_or_404(EtapeEvolution, id=id)
        etapeevolution.delete()
        return redirect('liste_EtapeEvolution')  # Redirection après suppression
    


def get_aliment_details(request, aliment_id):
    aliment = get_object_or_404(Aliment, id=aliment_id)
    if aliment.unite == 'kg':
        prix_par_g = int(aliment.prix_par_kg)/1000.0
    
    data = {
        'prix_par_kg': prix_par_g
    }
    
    return JsonResponse(data)


def ajouter_AlimentRecommande(request):
    if request.method == 'POST':
        form = AlimentRecommandeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_AlimentRecommande')  # Redirection vers la liste des poissons
    else:
        form = AlimentRecommandeForm()
    return render(request, 'alimentrecommande_ajout.html', {'form': form})


def liste_AlimentRecommande(request):
    alimentrecommandes = AlimentRecommande.objects.all()
    return render(request, 'alimentrecommande_liste.html', {'alimentrecommandes': alimentrecommandes})

def modifier_AlimentRecommande(request):
    id = request.GET.get('id')
    alimentrecommande = get_object_or_404(AlimentRecommande, id=id)
    if request.method == 'POST':
        form = AlimentRecommandeForm(request.POST, instance=alimentrecommande)
        if form.is_valid():
            form.save()
            return redirect('liste_AlimentRecommande')  # Redirection après modification
    else:
        form = AlimentRecommandeForm(instance=alimentrecommande)
    return render(request, 'alimentrecommande_modifier.html', {'form': form, 'alimentrecommande': alimentrecommande})


def supprimer_AlimentRecommande(request):
    
    if request.method == 'POST':
        id = request.POST.get('id')
        alimentrecommande = get_object_or_404(AlimentRecommande, id=id)
        alimentrecommande.delete()
        return redirect('liste_AlimentRecommande')  # Redirection après suppression
    

def ajouter_SuiviCroissance(request):
    if request.method == 'POST':
        form = SuiviCroissanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_SuiviCroissance')  # Redirection vers la liste des poissons
    else:
        form = SuiviCroissanceForm()
    return render(request, 'suivicroissance_ajout.html', {'form': form})


def liste_SuiviCroissance(request):
    suivicroissances = SuiviCroissance.objects.all()
    return render(request, 'suivicroissance_liste.html', {'suivicroissances': suivicroissances})

def modifier_SuiviCroissance(request):
    id = request.GET.get('id')
    suivicroissance = get_object_or_404(SuiviCroissance, id=id)
    if request.method == 'POST':
        form = SuiviCroissanceForm(request.POST, instance=suivicroissance)
        if form.is_valid():
            form.save()
            return redirect('liste_SuiviCroissance')  # Redirection après modification
    else:
        form = SuiviCroissanceForm(instance=suivicroissance)
    return render(request, 'suivicroissance_modifier.html', {'form': form, 'suivicroissance': suivicroissance})


def supprimer_SuiviCroissance(request):
    poisson_id = request.GET.get('id')
    suivicroissance = get_object_or_404(SuiviCroissance, id=poisson_id)
    if request.method == 'POST':
        suivicroissance.delete()
        return redirect('liste_SuiviCroissance')  # Redirection après suppression
    

def ajouter_pechedecalibrage(request):
    if request.method == 'POST':
        form = PecheDeCalibrageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_pechedecalibrage')  # Redirection vers la liste des poissons
    else:
        form = PecheDeCalibrageForm()
    return render(request, 'pechedecalibrage_ajout.html', {'form': form})


def liste_pechedecalibrage(request):
    pechedecalibrages = PecheDeCalibrage.objects.all()
    return render(request, 'pechedecalibrage_liste.html', {'pechedecalibrages': pechedecalibrages})

def modifier_pechedecalibrage(request):
    id = request.GET.get('id')
    pechedecalibrage = get_object_or_404(PecheDeCalibrage, id=id)
    if request.method == 'POST':
        form = PecheDeCalibrageForm(request.POST, instance=pechedecalibrage)
        if form.is_valid():
            form.save()
            return redirect('liste_pechedecalibrage')  # Redirection après modification
    else:
        form = PecheDeCalibrageForm(instance=pechedecalibrage)
    return render(request, 'pechedecalibrage_modifier.html', {'form': form, 'pechedecalibrage': pechedecalibrage})


def supprimer_pechedecalibrage(request):
    # Récupérer l'objet à supprimer
    peche_id = request.GET.get('id')
    pechedecalibrage = get_object_or_404(PecheDeCalibrage, id=peche_id)

    if request.method == 'POST':
        # Récupérer les objets liés avant suppression
        poisson = pechedecalibrage.poisson
        bande = poisson.bande  # Accéder à la bande associée

        # Rétablir les stocks
        poisson.nombre_poisson_dispo = F('nombre_poisson_dispo') + pechedecalibrage.quantite_peche
        poisson.save()

        bande.quantite_disponible_vente = F('quantite_disponible_vente') - pechedecalibrage.quantite_peche
        bande.save()

        # Supprimer l'instance
        pechedecalibrage.delete()

        # Redirection après suppression
        return redirect('liste_pechedecalibrage')

    # Affichage de la page de confirmation
    return render(request, 'supprimer_pechedecalibrage.html', {'pechedecalibrage': pechedecalibrage})

    


def ajouter_StockAlimentaire(request):
    if request.method == 'POST':
        form = StockAlimentaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_StockAlimentaire')  # Redirection vers la liste des poissons
    else:
        form = StockAlimentaireForm()
    return render(request, 'stockalimentaire_ajout.html', {'form': form})


def liste_StockAlimentaire(request):
    stockalimentaires = StockAlimentaire.objects.all()
    # stockalimentaires_totaux = StockAlimentaire.objects.values('aliment__nom').annotate(total_quantite=Sum('quantite_disponible'))
    context = {
        # 'stockalimentaires': stockalimentaires,
        'stockalimentaires_totaux':stockalimentaires
               }
    return render(request, 'stockalimentaire_liste.html',context)


def get_historique_stock(request, stock_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        historique = Historique_stock.objects.filter(stock_id=stock_id)
        data = [
            {
                "id": h.id,
                "stock": h.StockAlimentaire.aliment.nom,
                "quantite_ajoute": str(h.Montant),
                "date_mise_a_jour": h.dateajout.strftime("%Y-%m-%d"),
            }
            for h in historique
        ]
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Requête invalide"}, status=400)


def modifier_StockAlimentaire(request):
    id = request.GET.get('id')
    stockalimentaire = get_object_or_404(Historique_stock, id=id)
    if request.method == 'POST':
        form = StockAlimentaireForm(request.POST, instance=stockalimentaire)
        if form.is_valid():
            form.save()
            return redirect('liste_StockAlimentaire')  # Redirection après modification
    else:
        form = StockAlimentaireForm(instance=stockalimentaire)
    return render(request, 'stockalimentaire_modifier.html', {'form': form, 'stockalimentaire': stockalimentaire})


def supprimer_StockAlimentaire(request):
    poisson_id = request.GET.get('id')
    stockalimentaire = get_object_or_404(Historique_stock, id=poisson_id)
    if request.method == 'POST':
        stockalimentaire.delete()
        return redirect('liste_StockAlimentaire')  # Redirection après suppression
    


def ajouter_employe(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_employe')  # Redirection vers la liste des poissons
    else:
        form = EmployeForm()
    return render(request, 'employe_ajout.html', {'form': form})


def liste_employe(request):
    employes = Employe.objects.all()
    return render(request, 'Employe_liste.html', {'employes': employes})

def modifier_employe(request):
    id = request.GET.get('id')
    employe = get_object_or_404(Employe, id=id)
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            return redirect('liste_employe')  # Redirection après modification
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'employe_modifier.html', {'form': form, 'employe': employe})


def supprimer_employe(request, poisson_id):
    employe = get_object_or_404(Employe, id=poisson_id)
    if request.method == 'POST':
        employe.delete()
        return redirect('liste_employe')  # Redirection après suppression
    



def ajouter_vente(request):
    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ajouter_vente')  # Redirection vers la liste des poissons
    else:
        form = VenteForm()
    return render(request, 'vente_ajout.html', {'form': form})


def liste_vente(request):
    ventes = Vente.objects.all()
    return render(request, 'vente_liste.html', {'ventes': ventes})

def modifier_vente(request):
    id = request.GET.get('id')
    vente = get_object_or_404(Vente, id=id)
    if request.method == 'POST':
        form = VenteForm(request.POST, instance=vente)
        if form.is_valid():
            form.save()
            return redirect('liste_Vente')  # Redirection après modification
    else:
        form = VenteForm(instance=vente)
    return render(request, 'vente_modifier.html', {'form': form, 'vente': vente})


def supprimer_vente(request):
    poisson_id = request.GET.get('id')
    vente = get_object_or_404(Vente, id=poisson_id)
    if request.method == 'POST':
        vente.delete()
        return redirect('liste_Vente')  # Redirection après suppression
    

# def ajouter_depense(request):
#     if request.method == 'POST':
#         form = DepenseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('liste_depense')  # Redirection vers la liste des poissons
#     else:
#         form = DepenseForm()
#     return render(request, 'depense_ajout.html', {'form': form})

# def ajouter_depense(request):
#     if request.method == 'POST':
#         form = DepenseForm(request.POST, request.FILES)
#         if form.is_valid():
#             depense = form.save()
#             fichiers = request.FILES.getlist('fichiers')
#             if fichiers:  # Vérifiez si des fichiers sont présents
#                 for fichier in fichiers:
                    
#                     FichierDepense.objects.create(depense=depense, fichier=fichier)
#             else:
#                 print("Aucun fichier à ajouter.")
#             return redirect('ajouter_depense')
#     else:
#         form = DepenseForm()
#     return render(request, 'depense_ajout.html', {'form': form})


from django.contrib import messages


def ajouter_depense(request):
    if request.method == 'POST':
        form = DepenseForm(request.POST, request.FILES)
        if form.is_valid():
            # Récupérer les données du formulaire
            depense = form.save(commit=False)
            sourcefine = depense.sourcefine
            montant_depense = depense.montant

            # Vérifier si le solde de la source de financement est suffisant
            if sourcefine.solde < montant_depense:
                # Si le solde est insuffisant, afficher un message d'erreur et ne pas enregistrer la dépense
                messages.error(request, "Le solde de la source de financement est insuffisant pour cette dépense.")
                return redirect('ajouter_depense')  # Rediriger vers la page du formulaire

            # Enregistrer la dépense dans la base de données
            depense.save()

            # # Mettre à jour le solde de la source de financement
            # sourcefine.solde -= montant_depense
            # sourcefine.save()

            # Gestion des fichiers joints (si présents)
            fichiers = request.FILES.getlist('fichiers')
            if fichiers:  # Vérifiez si des fichiers sont présents
                for fichier in fichiers:
                    # Créer une entrée pour chaque fichier associé à la dépense
                    FichierDepense.objects.create(depense=depense, fichier=fichier)
            else:
                print("Aucun fichier à ajouter.")  # Optionnel, pour déboguer si nécessaire

            # Afficher un message de succès et rediriger
            messages.success(request, "La dépense a été ajoutée avec succès.")
            return redirect('ajouter_depense')  # Ou rediriger vers une autre page si nécessaire

    else:
        form = DepenseForm()  # Création du formulaire vide

    return render(request, 'depense_ajout.html', {'form': form})

def liste_depense(request):
    depenses = Depense.objects.all()
        # Calculer le total des dépenses pour le mois en cours
    mois_courant = now().month
    annee_courante = now().year
    total_depenses = Depense.objects.filter(
        date_depense__month=mois_courant, 
        date_depense__year=annee_courante
    ).aggregate(total=Sum('montant'))['total'] or 0
    seuil = seuil_depense(total_depenses)
    context = {
        'depenses': depenses,
        'seuil': seuil,
        }
    return render(request, 'depense_liste.html', context)

# def modifier_depense(request):
#     id = request.GET.get('id')
#     depense = get_object_or_404(Depense, id=id)
#     if request.method == 'POST':
#         form = DepenseForm(request.POST, instance=depense)
#         if form.is_valid():
#             form.save()
#             return redirect('liste_depense')  # Redirection après modification
#     else:
#         form = DepenseForm(instance=depense)
#     return render(request, 'depense_modifier.html', {'form': form, 'depense': depense})


def modifier_depense(request):
    id = request.GET.get('id')
    depense = get_object_or_404(Depense, id=id)
    fichiers_existants = depense.fichiers.all()  # Obtenir les fichiers associés à cette dépense

    if request.method == 'POST':
        form = DepenseForm(request.POST, request.FILES, instance=depense)
        if form.is_valid():
            depense = form.save()  # Enregistrez d'abord la dépense
            # Gérer les nouveaux fichiers
            nouveaux_fichiers = request.FILES.getlist('fichiers')  # Obtenez la liste des fichiers téléchargés
            if nouveaux_fichiers:  # Vérifiez si des fichiers sont présents
                for fichier in nouveaux_fichiers:
                    print(f"Ajout du fichier: {fichier.name}")  # Afficher le nom du fichier
                    FichierDepense.objects.create(depense=depense, fichier=fichier)  # Enregistrer le fichier
            else:
                print("Aucun fichier à ajouter.")
            return redirect('liste_depense')  # Remplacez par votre URL de redirection
    else:
        form = DepenseForm(instance=depense)  # Pré-remplir le formulaire avec les données de la dépense existante

    return render(request, 'depense_modifier.html', {'form': form, 'depense': depense, 'fichiers_existants': fichiers_existants})

def supprimer_depense(request):
    poisson_id = request.GET.get('id')
    depense = get_object_or_404(Depense, id=poisson_id)
    if request.method == 'POST':
        depense.delete()
        return redirect('liste_depense')  # Redirection après suppression
    


def ajouter_normecroissance(request):
    if request.method == 'POST':
        form = NormeCroissanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_normecroissance')  # Redirection vers la liste des poissons
    else:
        form = NormeCroissanceForm()
    return render(request, 'normecroissance_ajout.html', {'form': form})


def liste_normecroissance(request):
    normecroissances = NormeCroissance.objects.all()
    return render(request, 'normecroissance_liste.html', {'normecroissances': normecroissances})

def modifier_normecroissance(request):
    id = request.GET.get('id')
    normecroissance = get_object_or_404(NormeCroissance, id=id)
    if request.method == 'POST':
        form = NormeCroissanceForm(request.POST, instance=normecroissance)
        if form.is_valid():
            form.save()
            return redirect('liste_normecroissance')  # Redirection après modification
    else:
        form = NormeCroissanceForm(instance=normecroissance)
    return render(request, 'normecroissance_modifier.html', {'form': form, 'normecroissance': normecroissance})


def supprimer_normecroissance(request, poisson_id):
    vente = get_object_or_404(NormeCroissance, id=poisson_id)
    if request.method == 'POST':
        vente.delete()
        return redirect('liste_normecroissance')  # Redirection après suppression
    


def ajouter_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_client')  # Redirection vers la liste des poissons
    else:
        form = ClientForm()
    return render(request, 'client_ajout.html', {'form': form})


def liste_client(request):
    clients = Clients.objects.all()
    return render(request, 'client_liste.html', {'clients': clients})

def modifier_client(request):
    id = request.GET.get('id')
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('liste_client')  # Redirection après modification
    else:
        form = ClientForm(instance=client)
    return render(request, 'client_modifier.html', {'form': form, 'client': client})


def supprimer_client(request, poisson_id):
    client = get_object_or_404(Client, id=poisson_id)
    if request.method == 'POST':
        client.delete()
        return redirect('liste_client')  # Redirection après suppression
    



# def upload_fichier(request):
#     if request.method == 'POST':
#         form = FichierModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             fichier = form.cleaned_data['fichier']
#             nom = form.cleaned_data['nom']

#             # Créer l'instance de Fichier et encoder le fichier
#             fichier_obj = Fichier(nom=nom)
#             fichier_obj.encoder_et_sauvegarder(fichier.file)  # Encoder et sauvegarder le fichier en base64

#             return redirect('liste_upload_fichier')  # Redirection après succès
#     else:
#         form = FichierModelForm()

#     return render(request, 'upload_fichier.html', {'form': form})

# Vue de téléchargement du fichier
def upload_fichier(request):
    if request.method == 'POST':
        form = FichierModelForm(request.POST, request.FILES)
        if form.is_valid():
            fichier_instance = form.save(commit=False)
            fichier_instance.encoder_et_sauvegarder(request.FILES['fichier'])  # Appel de la méthode pour encoder et sauvegarder
            return redirect('liste_upload_fichier')
    else:
        form = FichierModelForm()
    return render(request, 'upload_fichier.html', {'form': form})



def liste_upload_fichier(request):
    upload_fichiers = Fichier.objects.all()
    return render(request, 'upload_fichier_liste.html', {'upload_fichiers': upload_fichiers})


def get_content_type(extension):
    """
    Retourne le type MIME basé sur l'extension du fichier.
    """
    mime_types = {
        'pdf': 'application/pdf',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        # Ajoute d'autres types MIME si nécessaire
    }
    return mime_types.get(extension, 'application/octet-stream')

# def download_file(request):
#     fichier_id = request.GET.get('id')
#     """
#     Vue pour afficher le fichier au lieu de le télécharger.
#     """
#     fichier_instance = Fichier.objects.get(id=fichier_id)
    
#     # Décoder les données base64
#     fichier_decode = base64.b64decode(fichier_instance.fichier_base64)
    
#     # Déterminer le type de contenu basé sur l'extension
#     content_type = get_content_type(fichier_instance.extension)
    
#     # Créer une réponse HTTP avec le contenu du fichier
#     response = HttpResponse(fichier_decode, content_type=content_type)
#     response['Content-Disposition'] = f'inline; filename="{fichier_instance.nom}.{fichier_instance.extension}"'
    
#     return response

def download_file(request, fichier_id):
    fichier_instance = Fichier.objects.get(id=fichier_id)
    
    # Récupérer et décompresser les données
    fichier_decode = fichier_instance.decoder_et_recuperer()
    
    # Créer une réponse HTTP avec le contenu du fichier
    response = HttpResponse(fichier_decode, content_type='application/octet-stream')
    response['Content-Disposition'] = f'inline; filename="{fichier_instance.nom}.{fichier_instance.extension}"'
    
    return response



def creer_bon_de_commande(request):
    bandes = Bande.objects.all()  # Récupérer tous les poissons
    stock_poissons_bandes = {bande.id: bande.quantite_disponible_vente for bande in bandes}
    poissons = Poisson.objects.all()  # Récupérer tous les poissons
    stock_poissons = {poisson.id: poisson.nombre_alevins for poisson in poissons}
    if request.method == 'POST':
        bon_form = BonDeCommandeForm(request.POST)
        if bon_form.is_valid():
            bon = bon_form.save()

            total_vente = 0  # Initialiser le total de la vente
            quantite_total = 0
            poids_total = 0
            # Récupérer les données des lignes du formulaire
            bande_ids = request.POST.getlist('poisson[]')
            quantites = request.POST.getlist('quantite[]')
            poids = request.POST.getlist('poids[]')
            prix_unitaires = request.POST.getlist('prix_unitaire[]')
            typepaiement = bon.typepaiement
            avance_montant = request.POST.get('avance_montant')
            # Traiter les lignes de commande
            for bande_id, quantite,poids, prix_unitaire in zip(bande_ids, quantites,poids, prix_unitaires):
                # try:

                if bande_id and poids and prix_unitaire:
                    quantite = float(quantite)
                    poids = float(poids)
                    prix_unitaire = float(prix_unitaire)
                    sous_total = poids * prix_unitaire

                    # Ajouter le sous-total au total de la vente
                    total_vente += sous_total
                    quantite_total +=quantite
                    poids_total +=poids


                    # intance_poisson = Poisson.objects.get(pk=bande_id)
                    intance_bande = Bande.objects.get(pk=bande_id)
                    # Créer la ligne de commande
                    LigneCommande.objects.create(
                        bon_de_commande=bon,
                        bande=intance_bande,
                        quantite=quantite,
                        poids=poids,
                        prix_unitaire=prix_unitaire,
                        sous_total=sous_total
                    )


                # except ValueError:
            if typepaiement == 'solde':
                # Enregistrer le total de la vente comme payé
                Paiement.objects.create(
                    bon_de_commande=bon,
                    montant_paye=total_vente,
                    date_paiement=bon.date_vente,
                )
                Vente.objects.create(
                    bon_de_commande = bon,
                    quantite_vendue=quantite_total,
                    Poids = poids_total,
                    prix_vente=total_vente,
                    montant_paye=total_vente,
                    reste_a_paye=total_vente,
                    date_vente=bon.date_vente,
                    date_solde=bon.date_vente,
                    client=bon.client
                        )
            elif typepaiement == 'avance':
                # Enregistrer une avance (montant total ici, ou spécifier une partie)
                Paiement.objects.create(
                    bon_de_commande=bon,
                    montant_paye=avance_montant,  # Variable pour une éventuelle saisie manuelle
                    date_paiement=bon.date_vente,
                )
                Vente.objects.create(
                    bon_de_commande = bon,
                    quantite_vendue=quantite_total,
                    Poids = poids_total,
                    prix_vente=total_vente,
                    montant_paye=avance_montant,
                    reste_a_paye=total_vente-avance_montant,
                    date_vente=bon.date_vente,
                    client=bon.client
                        )
            elif typepaiement == 'aucun':
                # Ne pas créer d'objet Paiement, mais enregistrer la vente

                Vente.objects.create(
                    bon_de_commande = bon,
                    quantite_vendue=quantite_total,
                    Poids = poids_total,
                    prix_vente=total_vente,
                    montant_paye=0,
                    reste_a_paye=total_vente,
                    date_vente=bon.date_vente,
                    client=bon.client
                        )
            
            return redirect('liste_vente')

    else:
        bon_form = BonDeCommandeForm()
        ligne_form = LigneBonDeCommandeForm()

    context = {
        'poissons': poissons,  # Passer la liste des poissons dans le contexte
        'stock_poissons':stock_poissons,
        'bandes': bandes,  
        'stock_poissons_bandes':stock_poissons_bandes,
        'bon_form': bon_form,
        'ligne_form': ligne_form,
    }

    return render(request, 'creer_bon_de_commande.html', context)


def enregistrer_paiement(request):

    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            ref_commande = request.POST.get('ref_bon')
            bon_de_commande = BonDeCommande.objects.get(ref_bon=ref_commande)
            paiement = form.save(commit=False)
            paiement.bon_de_commande = bon_de_commande
            paiement.save()
            return redirect('liste_vente')  # Rediriger vers une page de votre choix
    else:

        form = PaiementForm()

    # Passer les données supplémentaires au contexte
    ref_commande = request.GET.get('id')

    bon_de_commande = BonDeCommande.objects.get(ref_bon=ref_commande)
    
    vente = Vente.objects.filter(bon_de_commande=bon_de_commande).first()  # Supposant qu'il y a une relation
    
    context = {
        'form': form,
        'bon_de_commande': bon_de_commande,
        'vente': vente,
    }
    return render(request, 'creer_paiement.html', context)



def details_bon_de_commande(request):
    
    if request.method == 'GET':
        bon_id = request.GET.get('id')
        
        if bon_id:
            try:
                bon_de_commande = BonDeCommande.objects.get(id=bon_id)
                lignes_commande = LigneCommande.objects.filter(bon_de_commande=bon_de_commande)
                
                context = {
                    'bon_de_commande': bon_de_commande,
                    'lignes_commande': lignes_commande,
                }
                return render(request, 'details_bon_de_commande.html', context)
            except BonDeCommande.DoesNotExist:
                return JsonResponse({'error': 'Bon de commande non trouvé.'}, status=404)
        else:
            return JsonResponse({'error': 'ID de bon de commande manquant.'}, status=400)



def calculer_cout_alimentaire(espece, quantite_poissons):
    # Récupérer les recommandations d'aliments pour l'espèce donnée
    recommandations = AlimentRecommande.objects.filter(espece=espece)
    
    # Calculer la somme des quantités et des prix pour chaque recommandation
    # total_quantite_recommandee = recommandations.aggregate(total_quantite=Sum('quantite_recommandee'))['total_quantite'] or 0
    total_cout_aliments = recommandations.aggregate(total_cout=Sum('prix'))['total_cout'] or 0
    quantite_poissons = quantite_poissons[0]
    # Calculer le coût total pour la quantité de poissons donnée
    cout_total_par_jour = int(total_cout_aliments) * int(quantite_poissons)
    
    return cout_total_par_jour


# def calculer_previsions(request):
#     if request.method == 'POST':
#         form = BeneficeCibleForm(request.POST)
#         if form.is_valid():
#             espece = form.cleaned_data['espece']
#             benefice_cible = form.cleaned_data['benefice_cible']
#             prix_vente_par_kg = form.cleaned_data['prix_vente_par_kg']
#             taux_mortalite = form.cleaned_data['taux_mortalite']
#             duree_elevage = form.cleaned_data['duree_elevage']
            
#             # Calculer la quantité nécessaire pour atteindre l'objectif
#             quantite_nec = benefice_cible / prix_vente_par_kg
            
#             # Calculer le coût total des aliments

#             cout_total_aliments = calculer_cout_alimentaire(espece, quantite_nec)
#             couts_production = 0
#             # Calculer d'autres coûts de production (exemple)
#             couts_production = Depense.objects.aggregate(total_cost=Sum('montant'))['total_cost']
#             if couts_production is None:
#                 couts_production = 0

#             # Calculer les dépenses prévisionnelles
#             depenses_previsionnelles = cout_total_aliments + couts_production
            
#             context = {
#                 'quantite_nec': quantite_nec,
#                 'prix_vente_par_kg': prix_vente_par_kg,
#                 'taux_mortalite': taux_mortalite,
#                 'duree_elevage': duree_elevage,
#                 'depenses_previsionnelles': depenses_previsionnelles,
#             }
#             return render(request, 'resultats_calcul.html', context)
#     else:
#         form = BeneficeCibleForm()
    
#     return render(request, 'calcul_benefice.html', {'form': form})

# def calculer_previsions(request):
#     if request.method == 'POST':
#         form = BeneficeCibleForm(request.POST)
#         if form.is_valid():
#             espece = form.cleaned_data['espece']
#             benefice_cible = form.cleaned_data['benefice_cible']
#             prix_vente_par_kg = form.cleaned_data['prix_vente_par_kg']
#             taux_mortalite = form.cleaned_data['taux_mortalite'] / 100  # en pourcentage
#             duree_elevage = form.cleaned_data['duree_elevage']

#             # Estimation initiale de la quantité nécessaire pour atteindre le bénéfice
#             quantite_nec = benefice_cible / prix_vente_par_kg

#             # Calculer le coût alimentaire pour cette quantité de poissons
#             cout_aliment_jour = calculer_cout_alimentaire(espece, quantite_nec)
#             cout_total_aliments = cout_aliment_jour * duree_elevage

#             # Ajouter les autres coûts de production (ex. soins, infrastructure)
#             couts_production = Depense.objects.aggregate(total_cost=Sum('montant'))['total_cost'] or 0

#             # Dépenses totales = coût alimentaire + autres coûts de production
#             depenses_previsionnelles = cout_total_aliments + couts_production

#             # Recalculer la quantité en tenant compte des coûts de production
#             quantite_nec_finale = (int(benefice_cible) + int(depenses_previsionnelles)) / int(prix_vente_par_kg)

#             # Ajuster la quantité en fonction du taux de mortalité
#             quantite_nec_initiale = float(quantite_nec_finale) / float(1 - taux_mortalite)

#             # Calcul du montant total des pré-ventes
#             montant_pre_vente = float(benefice_cible) + float(depenses_previsionnelles)

#             context = {
#                 'montant_pre_vente': montant_pre_vente,
#                 'quantite_nec_initial': quantite_nec_initiale,
#                 'benefice_cible': benefice_cible,
#                 'quantite_nec_finale': quantite_nec_finale,
#                 'prix_vente_par_kg': prix_vente_par_kg,
#                 'taux_mortalite': taux_mortalite * 100,  # retour en pourcentage
#                 'duree_elevage': duree_elevage,
#                 'depenses_previsionnelles': depenses_previsionnelles,
#             }
#             return render(request, 'resultats_calcul.html', context)
#     else:
#         form = BeneficeCibleForm()

#     return render(request, 'calcul_benefice.html', {'form': form})






def generedata(espece):

    # Génération de données fictives pour tester le modèle
    np.random.seed(42)

    n = 100  # nombre de données
    benefice_cible = np.random.uniform(5000000, 50000000, n)
    prix_vente_par_kg = np.random.uniform(2000, 3000, n)
    taux_mortalite = np.random.uniform(0.05, 0.1, n)
    duree_elevage = np.random.uniform(90, 180, n)
    
    # Supposons que cout_alimentaire_total soit une fonction qui calcule le coût alimentaire pour une durée donnée

    
# Initialiser une première estimation de l'investissement total
    investissement_total_initial = benefice_cible * 0.7  # ou un autre calcul approximatif

    # Maintenant, calculez quantite_poisson_nec
    quantite_poisson_nec = (benefice_cible + investissement_total_initial) / prix_vente_par_kg

# Ensuite, calculez cout_alimentaire_total, soins_total, et finalement l'investissement_total


    cout_alimentaire_total = calculer_cout_alimentaire(espece, quantite_poisson_nec) * duree_elevage

    # cout_soins_par_poisson = Depense.objects.aggregate(total_cost=Sum('montant'))['total_cost'] or 0


    # Calculer l'investissement total sbasé sur des règles fictives
    investissement_total = (
        (benefice_cible * 0.7) + 
        # (prix_vente_par_kg * quantite_poisson_nec) +  # Ajustement selon le nombre de poissons
        (cout_alimentaire_total) + 
        (duree_elevage * taux_mortalite * 200)
        # + cout_soins_par_poisson  # Ajout d'autres dépenses
    )


    # Créer un DataFrame avec les données générées
    data = pd.DataFrame({
        'benefice_cible': benefice_cible,
        'prix_vente_par_kg': prix_vente_par_kg,
        'taux_mortalite': taux_mortalite,
        'duree_elevage': duree_elevage,
        'investissement_total': investissement_total,
        'quantite_poisson_nec': quantite_poisson_nec
    })

    # Afficher les premières lignes
    print(data.head())

    # Enregistrer les données dans un fichier CSV pour des tests
    data.to_csv('donnees_pisciculture_simulees.csv', index=False)



# Exemple de données d'entraînement (historique)


# Fonction de prévision avec les deux modèles de régression
def calculer_previsions(request):
    if request.method == 'POST':
        form = BeneficeCibleForm(request.POST)
        form1 = VariablecibleForm(request.POST)
        if form.is_valid():
            espece = form.cleaned_data['espece']
            benefice_cible = form.cleaned_data['benefice_cible']
            prix_vente_par_kg = form.cleaned_data['prix_vente_par_kg']
            taux_mortalite = form.cleaned_data['taux_mortalite'] / 100  # Convertir en pourcentage
            duree_elevage = form.cleaned_data['duree_elevage']

            # Préparer les données pour la prédiction
            X_input = pd.DataFrame({
                'benefice_cible': [benefice_cible],
                'prix_vente_par_kg': [prix_vente_par_kg],
                'taux_mortalite': [taux_mortalite],
                'duree_elevage': [duree_elevage]
            })

     

            data = pd.read_csv('pisciculture_cycles.csv')
            
            # Séparer les données en variables explicatives (X) et variables cibles (y)
            X = data[['benefice_cible', 'prix_vente_par_kg', 'taux_mortalite', 'duree_elevage']]

            # Modèle pour prédire l'investissement total
            y_investissement = data['investissement_total']
            model_investissement = LinearRegression()
            model_investissement.fit(X, y_investissement)

            # Modèle pour prédire la quantité de poisson nécessaire
            y_quantite = data['Poids_Poisson_kg']
            model_quantite = LinearRegression()
            model_quantite.fit(X, y_quantite)

            print("Coefficients pour l'investissement total :", model_investissement.coef_)



            # Prédire l'investissement total nécessaire
            investissement_pred = model_investissement.predict(X_input)[0]
            montant_pre_vente = int(investissement_pred) + int(benefice_cible)
            # Prédire la quantité de poisson nécessaire
            quantite_poisson_pred = model_quantite.predict(X_input)[0]

            # Ajuster la quantité en fonction du taux de mortalité
            quantite_poisson_nec = float(quantite_poisson_pred) * float(1 + taux_mortalite)

            context = {
                'benefice_cible': benefice_cible,
                'montant_pre_vente': montant_pre_vente,
                'prix_vente_par_kg': prix_vente_par_kg,
                'taux_mortalite': taux_mortalite * 100,  # Retour au pourcentage pour l'affichage
                'duree_elevage': duree_elevage,
                'depenses_previsionnelles': investissement_pred,
                'quantite_poisson_nec': quantite_poisson_nec,
                'quantite_poisson_pred': quantite_poisson_pred,
            }
            return render(request, 'resultats_calcul.html', context)
    else:
        form = BeneficeCibleForm()
    
    return render(request, 'calcul_benefice.html', {'form': form})


def csv():

    # Créer un tableau avec des données réalistes pour 20 cycles
    data = {
        "benefice_cible": [68500000, 70000000, 72000000, 74000000, 75000000, 
                        76000000, 78000000, 79000000, 80000000, 81000000,
                        82000000, 83000000, 84000000, 85000000, 86000000,
                        87000000, 88000000, 89000000, 90000000, 91000000, 
                        92000000],
        "prix_vente_par_kg": [3000, 3100, 3200, 3300, 3400,
                            3500, 3600, 3700, 3800, 3900,
                            4000, 4100, 4200, 4300, 4400,
                            4500, 4600, 4700, 4800, 4900,
                            5000],
        "taux_mortalite": [10, 10, 10, 10, 10,
                        10, 10, 10, 10, 10,
                        10, 10, 10, 10, 10,
                        10, 10, 10, 10, 10],
        "duree_elevage": [6, 6, 6, 6, 6,
                        6, 6, 6, 6, 6,
                        6, 6, 6, 6, 6,
                        6, 6, 6, 6, 6],
        "investissement_total": [127523815, 100000000, 105000000, 110000000, 115000000,
                                120000000, 125000000, 130000000, 135000000, 140000000,
                                145000000, 150000000, 155000000, 160000000, 165000000,
                                170000000, 175000000, 180000000, 185000000, 190000000,
                                195000000],
        "quantite_poisson_nec": [2000, 2100, 2200, 2300, 2400,
                                2500, 2600, 2700, 2800, 2900,
                                3000, 3100, 3200, 3300, 3400,
                                3500, 3600, 3700, 3800, 3900,
                                4000],
        "poids_poisson": [3000, 3150, 3300, 3450, 3600,
                        3750, 3900, 4050, 4200, 4350,
                        4500, 4650, 4800, 4950, 5100,
                        5250, 5400, 5550, 5700, 5850,
                        6000],
    }

    # Créer un DataFrame
    df = pd.DataFrame(data)

    # Enregistrer le DataFrame en fichier CSV
    file_path = 'donnees_pisciculture.csv'
    df.to_csv(file_path, index=False)

    file_path

# csv()

import os

# def afficher_pdf(request):
#     # Charger le fichier Excel
    
#     fichier_excel = 'C:/Users/HP/Downloads/RAPPORT V2/CF ATTOH/Liste des BON LIQ MDT traités par le CF ATTOH sur 2024 MSHP.xlsx'
#     df = pd.read_excel(fichier_excel)
    
#     # Répertoire des PDF
#     pdf_directory = 'C:/Users/HP/Downloads/RAPPORT V2/CF ATTOH/'
    
#     # Ajouter les liens vers les fichiers PDF
#     df['pdf_link'] = df['Numero_du_document'].apply(lambda x: os.path.join(pdf_directory, f'{x}.pdf'))
    
#     # Vérifier l'existence des fichiers et créer les liens
#     df['pdf_exists'] = df['pdf_link'].apply(lambda x: os.path.exists(x))
#     df['lien_pdf'] = df.apply(lambda row: row['pdf_link'] if row['pdf_exists'] else 'PDF non trouvé', axis=1)
    
#     # Enregistrer le fichier Excel mis à jour
#     df.to_excel(fichier_excel, index=False)
    
#     # Retourner une réponse indiquant que le fichier a été mis à jour
#     return HttpResponse("Le fichier Excel a été mis à jour avec les liens vers les fichiers PDF.")


def send_sms(msg):
    url = "https://apis.letexto.com/v1/campaigns/sms"
    payload = json.dumps({
    "label": "Notification des ventes et dépenses",
    "sender": "SIGACQ SGCI",
    "contacts": [
        # {
        # "numero": "2250789248701",
        # },
        {
          "numero": "2250544169597",
        },
        # {
        #   "age": "32",
        #   "numero": "2250000000000",
        #   "name": "John"
        # }
    ],
    "content": msg
    })
    headers = {
    'Authorization': 'Bearer 34b7559f677cd31a16746a20ad1ae7',
    'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()  # Vérifie si l'API renvoie une erreur HTTP
        # data = response.json()
        # print(json.dumps(data))
    except requests.exceptions.RequestException as e:
        print(f"Erreur d'envoi SMS : {e}")

    # response = requests.post(url, data=payload, headers=headers)
    # data = response.json()
    # print(json.dumps(data))


# send_sms("Bonjour Armand. Cet SMS t'a été envoyé dépuis l'outil de gestion piscicolte","2250544169597")


def ajouter_historique_sourcefine(request):
    if request.method == 'POST':
        form = Historique_sourcefineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_sourcefine')  # Redirection vers la liste des poissons
    else:
        form = Historique_sourcefineForm()
    return render(request, 'historique_sourcefine_ajout.html', {'form': form})



def get_historique_sourcefine(request, sourcefine_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        historique = Historique_Sourcefine.objects.filter(sourcefine_id=sourcefine_id)
        data = [
            {
                "id": h.id,
                "sourcefine": h.sourcefine.nom,
                "Montant": str(h.Montant),
                "dateajout": h.dateajout.strftime("%Y-%m-%d"),
                "datemotif": h.datemotif.strftime("%Y-%m-%d")
            }
            for h in historique
        ]
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Requête invalide"}, status=400)


def modifier_historique_sourcefine(request,id):
    
    historique_sourcefine = get_object_or_404(Historique_Sourcefine, id=id)
    if request.method == 'POST':
        form = Historique_sourcefineForm(request.POST, instance=historique_sourcefine)
        if form.is_valid():
            form.save()
            return redirect('liste_sourcefine')  # Redirection après modification
    else:
        form = Historique_sourcefineForm(instance=historique_sourcefine)
    return render(request, 'historique_sourcefine_modifier.html', {'form': form, 'historique_sourcefine': historique_sourcefine})


def supprimer_historique_sourcefine(request,id):
    historique_sourcefine = get_object_or_404(Historique_Sourcefine, id=id)
    if request.method == 'DELETE':
        historique_sourcefine.delete()
        return redirect('liste_sourcefine')  # Redirection après suppression



def liste_sourcefine(request):
    sourcefines = Sourcefine.objects.all()
    context = {
        'sourcefines':sourcefines,
    }
    return render(request, 'sourcefine_liste.html',context)


def modifier_sourcefine(request):
    id = request.GET.get('id')
    sourcefine = get_object_or_404(Sourcefine, id=id)
    if request.method == 'POST':
        form = SourcefineForm(request.POST, instance=sourcefine)
        if form.is_valid():
            form.save()
            return redirect('liste_sourcefine')  # Redirection après modification
    else:
        form = SourcefineForm(instance=sourcefine)
    return render(request, 'sourcefine_modifier.html', {'form': form, 'sourcefine': sourcefine})


def supprimer_sourcefine(request):
    sourcefine_id = request.GET.get('id')
    historique_sourcefine = get_object_or_404(Sourcefine, id=sourcefine_id)
    if request.method == 'GET':
        historique_sourcefine.delete()
        return redirect('liste_sourcefine')  # Redirection après suppression



def valider_demande_reduction(request, demande_id, validation_step):
    """
    API pour valider une demande de réduction à une étape spécifique.
    """
    demande = get_object_or_404(demandeReduction, pk=demande_id)

    # Validation de l'étape
    if validation_step not in ['v1', 'v2', 'v3']:
        return HttpResponseBadRequest("Étape de validation non valide.")

    # Marquer l'étape comme validée
    setattr(demande, validation_step, True)
    demande.save()

    # Vérification si toutes les validations sont complétées
    if demande.v1 and demande.v2 and demande.v3:
        demande.valide = True
        demande.save()

    return JsonResponse({
        "message": f"Validation {validation_step} complétée.",
        "valide": demande.valide,
    })


def envoyer_lien_validation(demande):
    """
    Envoie des SMS aux trois responsables pour la validation.
    """
    responsables = [
        {'nom': 'Monsieur le Directeur', 'numero': '+2250544169597', 'etape': 'v1'},
        {'nom': 'Monsieur le Directeur', 'numero': '+2250544169597', 'etape': 'v2'},
        {'nom': 'Monsieur le Directeur', 'numero': '+2250544169597', 'etape': 'v3'},
    ]

    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    for responsable in responsables:
        lien = demande.get_validation_link(responsable['etape'])
        message = f"Bonjour {responsable['nom']}, veuillez valider la demande de réduction via ce lien : {settings.SITE_URL}{lien}"
        
        send_sms(message)
        # client.messages.create(
        #     body=message,
        #     from_=settings.TWILIO_PHONE_NUMBER,
        #     to=responsable['numero']
        # )
        


def creer_demande_reduction(request):
    if request.method == 'POST':
        form = DemandeReductionForm(request.POST)
        if form.is_valid():
            # Sauvegarder la demande de réduction
            demande = form.save()
            
            # Envoyer les liens de validation par SMS
            envoyer_lien_validation(demande)
            
            messages.success(request, "Demande de réduction enregistrée et liens de validation envoyés.")
            return redirect('liste_client')  # Redirection après succès
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = DemandeReductionForm()
    
    return render(request, 'creer_demande_reduction.html', {'form': form})



def check_reduction(request):
    client_id = request.GET.get('client_id')
    try:
        reduction = demandeReduction.objects.filter(client_id=client_id, valide=True).first()
        if reduction:
            return JsonResponse({
                'reduction_valid': True,
                'cout_total': reduction.cout_reduction,
            })
        else:
            return JsonResponse({'reduction_valid': False})
    except reduction.DoesNotExist:
        return JsonResponse({'reduction_valid': False})
