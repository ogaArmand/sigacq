from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *
from .forms import *


# class Fichieradmin(admin.ModelAdmin):
#     list_display = ('nom','extension','fichier_base64')

# admin.site.register(Fichier,Fichieradmin)


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('seuil_depense',)
    
admin.site.register(Fichier)
admin.site.register(Client)
admin.site.register(BonDeCommande)
admin.site.register(LigneCommande)
admin.site.register(Bassin)
admin.site.register(superficie)
admin.site.register(Vente)
admin.site.register(Depense)
admin.site.register(FichierDepense)
admin.site.register(Souche)
admin.site.register(EspecePoisson)
admin.site.register(Stade)
admin.site.register(NormeCroissance)
admin.site.register(EtapeEvolution)
admin.site.register(AlimentRecommande)
admin.site.register(SuiviCroissance)



admin.site.site_header = 'Administration sigacquat'
admin.site.site_title = 'sigacquat'