"""fada URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gestion_pisciculture.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from gestion_pisciculture import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('loginuser',loginuser,name='loginuser'),
    path('open_admin', open_admin, name='open_admin'),
    path('create_account', create_account, name='create_account'),
    path('', accueil, name='accueil'),
    path('connexion', connexion, name='connexion'),
    path('bassin', bassin, name='bassin'),
    path('liste_bassins', liste_bassins, name='liste_bassins'),
    path('modifier_bassin', modifier_bassin, name='modifier_bassin'),
    path('supprimer_bassin/<int:id>/', views.supprimer_bassin, name='supprimer_bassin'),
    path('ajouter_bande', ajouter_bande, name='ajouter_bande'),
    path('liste_bande', liste_bande, name='liste_bande'),
    path('modifier_bande', modifier_bande, name='modifier_bande'),
    path('supprimer_bande/<int:id>/', views.supprimer_bande, name='supprimer_bande'),
    path('Ajoutespece', Ajoutespece, name='Ajoutespece'),
    path('liste_espece', liste_espece, name='liste_espece'),
    path('modifier_espece', modifier_espece, name='modifier_espece'),
    path('supprimer_espece', views.supprimer_espece, name='supprimer_espece'),
    path('ajouter_poisson', ajouter_poisson, name='ajouter_poisson'),
    path('liste_poisson', liste_poisson, name='liste_poisson'),
    path('modifier_poisson', modifier_poisson, name='modifier_poisson'),
    path('supprimer_poisson', views.supprimer_poisson, name='supprimer_poisson'),
    path('ajouter_mortalite', ajouter_mortalite, name='ajouter_mortalite'),
    path('liste_mortalite', liste_mortalite, name='liste_mortalite'),
    path('modifier_mortalite', modifier_mortalite, name='modifier_mortalite'),
    path('supprimer_mortalite', views.supprimer_mortalite, name='supprimer_mortalite'),
    path('ajouter_nourrirpoisson', ajouter_nourrirpoisson, name='ajouter_nourrirpoisson'),
    path('liste_nourrirpoisson', liste_nourrirpoisson, name='liste_nourrirpoisson'),
    path('modifier_nourrirpoisson', modifier_nourrirpoisson, name='modifier_nourrirpoisson'),
    path('supprimer_nourrirpoisson', views.supprimer_nourrirpoisson, name='supprimer_nourrirpoisson'),
    path('Ajout_aliment', Ajout_aliment, name='Ajout_aliment'),
    path('liste_aliment', liste_aliment, name='liste_aliment'),
    path('modifier_aliment', modifier_aliment, name='modifier_aliment'),
    path('supprimer_aliment/<int:id>/', views.supprimer_aliment, name='supprimer_aliment'),
    path('ajouter_RationAlimentaire', ajouter_RationAlimentaire, name='ajouter_RationAlimentaire'),
    path('distribuer_ration/<int:id>/', views.distribuer_ration, name='distribuer_ration'),
     path('get_aliment_details/<int:aliment_id>/', views.get_aliment_details, name='get_aliment_details'),
    path('liste_RationAlimentaire', liste_RationAlimentaire, name='liste_RationAlimentaire'),
    path('modifier_RationAlimentaire', modifier_RationAlimentaire, name='modifier_RationAlimentaire'),
    path('supprimer_RationAlimentaire', views.supprimer_RationAlimentaire, name='supprimer_RationAlimentaire'),
    path('ajouter_SuiviCroissance', ajouter_SuiviCroissance, name='ajouter_SuiviCroissance'),
    path('liste_SuiviCroissance', liste_SuiviCroissance, name='liste_SuiviCroissance'),
    path('modifier_SuiviCroissance', modifier_SuiviCroissance, name='modifier_SuiviCroissance'),
    path('supprimer_SuiviCroissance', views.supprimer_SuiviCroissance, name='supprimer_SuiviCroissance'),
    path('ajouter_pechedecalibrage', ajouter_pechedecalibrage, name='ajouter_pechedecalibrage'),
    path('liste_pechedecalibrage', liste_pechedecalibrage, name='liste_pechedecalibrage'),
    path('modifier_pechedecalibrage', modifier_pechedecalibrage, name='modifier_pechedecalibrage'),
    path('supprimer_pechedecalibrage', views.supprimer_pechedecalibrage, name='supprimer_pechedecalibrage'),
    path('ajouter_StockAlimentaire', ajouter_StockAlimentaire, name='ajouter_StockAlimentaire'),
    path('liste_StockAlimentaire', liste_StockAlimentaire, name='liste_StockAlimentaire'),
    path('modifier_StockAlimentaire/<int:id>/', modifier_StockAlimentaire, name='modifier_StockAlimentaire'),
    path('supprimer_StockAlimentaire/<int:id>/', views.supprimer_StockAlimentaire, name='supprimer_StockAlimentaire'),
    path('ajouter_employe', ajouter_employe, name='ajouter_employe'),
    path('liste_employe', liste_employe, name='liste_employe'),
    path('modifier_employe', modifier_employe, name='modifier_employe'),
    path('supprimer_employe', views.supprimer_employe, name='supprimer_employe'),
    path('ajouter_vente', ajouter_vente, name='ajouter_vente'),
    path('liste_vente', liste_vente, name='liste_vente'),
    path('modifier_vente', modifier_vente, name='modifier_vente'),
    path('supprimer_vente', views.supprimer_vente, name='supprimer_vente'),
    path('ajouter_depense', ajouter_depense, name='ajouter_depense'),
    path('liste_depense', liste_depense, name='liste_depense'),
    path('modifier_depense', modifier_depense, name='modifier_depense'),
    path('supprimer_depense', views.supprimer_depense, name='supprimer_depense'),
    path('ajouter_EtapeEvolution', ajouter_EtapeEvolution, name='ajouter_EtapeEvolution'),
    path('liste_EtapeEvolution', liste_EtapeEvolution, name='liste_EtapeEvolution'),
    path('modifier_EtapeEvolution', modifier_EtapeEvolution, name='modifier_EtapeEvolution'),
    path('supprimer_EtapeEvolution', views.supprimer_EtapeEvolution, name='supprimer_EtapeEvolution'),
    path('ajouter_AlimentRecommande', ajouter_AlimentRecommande, name='ajouter_AlimentRecommande'),
    path('liste_AlimentRecommande', liste_AlimentRecommande, name='liste_AlimentRecommande'),
    path('modifier_AlimentRecommande', modifier_AlimentRecommande, name='modifier_AlimentRecommande'),
    path('supprimer_AlimentRecommande', views.supprimer_AlimentRecommande, name='supprimer_AlimentRecommande'),
    path('ajouter_normecroissance', ajouter_normecroissance, name='ajouter_normecroissance'),
    path('liste_normecroissance', liste_normecroissance, name='liste_normecroissance'),
    path('modifier_normecroissance', modifier_normecroissance, name='modifier_normecroissance'),
    path('upload_fichier', upload_fichier, name='upload_fichier'),
    path('download_file', download_file, name='download_file'),
    path('liste_upload_fichier', liste_upload_fichier, name='liste_upload_fichier'),
    path('supprimer_normecroissance', views.supprimer_normecroissance, name='supprimer_normecroissance'),
    path('creer_bon_de_commande', creer_bon_de_commande, name='creer_bon_de_commande'),
    path('enregistrer_paiement', enregistrer_paiement, name='enregistrer_paiement'),
    path('details_bon_de_commande/', views.details_bon_de_commande, name='details_bon_de_commande'),
    path('ajouter_client', ajouter_client, name='ajouter_client'),
    path('liste_client', liste_client, name='liste_client'),
    path('modifier_client', modifier_client, name='modifier_client'),
    path('ajouter_historique_sourcefine', ajouter_historique_sourcefine, name='ajouter_historique_sourcefine'),
    path('get_historique_sourcefine/<int:sourcefine_id>/', views.get_historique_sourcefine, name='get_historique_sourcefine'),
    path('get_historique_stock/<int:stock_id>/', views.get_historique_stock, name='get_historique_stock'),
    path('get_historique_stock_sorti/<int:stock_id>/', views.get_historique_stock_sorti, name='get_historique_stock_sorti'),
    path('modifier_historique_sourcefine/<int:id>/', modifier_historique_sourcefine, name='modifier_historique_sourcefine'),
    path('supprimer_historique_sourcefine/<int:id>/', supprimer_historique_sourcefine, name='supprimer_historique_sourcefine'),
    path('get-etapes-actives/', views.get_etapes_actives, name='get_etapes_actives'),
    path('liste_sourcefine', liste_sourcefine, name='liste_sourcefine'),
    path('modifier_sourcefine', modifier_sourcefine, name='modifier_sourcefine'),
    path('supprimer_sourcefine', supprimer_sourcefine, name='supprimer_sourcefine'),
    path('calculer_previsions', calculer_previsions, name='calculer_previsions'),
    path('creer_demande_reduction', creer_demande_reduction, name='creer_demande_reduction'),
    path(
        'valider_demande/<int:demande_id>/<str:validation_step>/',
        valider_demande_reduction,
        name='valider_demande_reduction'
    ),
    path('api/check_reduction', views.check_reduction, name='check_reduction'),
    # path('afficher_pdf', afficher_pdf, name='afficher_pdf'),
    path('supprimer_client', views.supprimer_client, name='supprimer_client'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('loginuser')), name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

