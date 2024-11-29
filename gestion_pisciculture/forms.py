from django import forms
from .models import *
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError

class BandeForm(forms.ModelForm):
    class Meta:
        model = Bande
        fields = ['especepoisson', 'quantite_init', 'quantite_transfere', 'quantite_restante', 'mortalite', 'date_introduction','date_fin_prevu','date_fin_reel']
        widgets = {
    'especepoisson': forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'Espece de poisson',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'quantite_init': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Quantité initiale',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'quantite_transfere': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Quantité empoissonée',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'quantite_restante': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Quantité restante',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'mortalite': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Taux de mortalité',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'date_introduction': forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'date_fin_prevu': forms.NumberInput(attrs={
        'type': 'date',
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'date_fin_reel': forms.NumberInput(attrs={
        'type': 'date',
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}

class BassinForm(forms.ModelForm):
    class Meta:
        model = Bassin
        fields = ['nom', 'superficie', 'contenu_reel', 'capacite_eau_reel', 'temperature_courante', 'description']
        widgets = {
    'nom': forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Nom de l''étang',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'superficie': forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'superficie',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'contenu_reel': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Contenu réel',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'capacite_eau_reel': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Capacité en eau',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'temperature_courante': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Température courante',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'description': forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': 'Description',
        'rows': 3,
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}


class especeForm(forms.ModelForm):
    class Meta:
        model = EspecePoisson
        fields = ['nom', 'souche', 'indice_conversion', 'description']
        widgets = {
    'nom': forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Saisissez le nom de l''espèce',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'souche': forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'Sélectionnez la souche',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'indice_conversion': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Indice de conversion',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'description': forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': 'description',
        'rows':3,
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

}
        
class PoissonForm(forms.ModelForm):
    class Meta:
        model = Poisson
        fields = ['espece', 'bande', 'bassin', 'date_introduction', 'poids_initial', 'poids_actuel', 'nombre_alevins', 'taux_mortalite']
        widgets = {
    'espece': forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'Nom du bassin',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'bande': forms.Select(attrs={
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'bassin': forms.Select(attrs={
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'poids_initial': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'poids moyen initial (g)',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'poids_actuel': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'poids actuel',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'nombre_alevins': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'nombre d''alevins',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'taux_mortalite': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'nombre de mortalité',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'date_introduction': forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}


class NourrirpoissonForm(forms.ModelForm):
    class Meta:
        model = Nourrirpoisson
        fields = ['poisson', 'etapeevolution', 'aliment', 'rationalimentaire_donnee', 'date_alimentation_reel']
        widgets = {
            'poisson': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Lot de poisson',
                'style': 'font-size: 20px; color: #043372; font-weight: bold;'
            }),

            'etapeevolution': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'font-size: 20px; color: #043372; font-weight: bold;'
            }),
            'aliment': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'font-size: 20px; color: #043372; font-weight: bold;'
            }),
            'rationalimentaire_donnee': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ration servie',
                'style': 'font-size: 20px; color: #043372; font-weight: bold;'
            }),
            'date_alimentation_reel': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control', 
                'style': 'font-size: 20px; color: #043372; font-weight: bold;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'poisson' in self.data:
            # Si un poisson est sélectionné dans le formulaire
            try:
                poisson_id = int(self.data.get('poisson'))
                
                etapes_actives = EtapeEvolution.objects.filter(poisson_id=poisson_id, etat=True)
                self.fields['etapeevolution'].queryset = etapes_actives
                if etapes_actives.exists():
                    # Sélectionne l'étape active par défaut
                    self.initial['etapeevolution'] = etapes_actives.first()
            except (ValueError, TypeError):
                self.fields['etapeevolution'].queryset = EtapeEvolution.objects.none()
        elif self.instance.pk:
            # Si le formulaire est lié à une instance existante
            etapes_actives = EtapeEvolution.objects.filter(poisson=self.instance.poisson, etat=True)
            self.fields['etapeevolution'].queryset = etapes_actives
            if etapes_actives.exists() and not self.initial.get('etapeevolution'):
                self.initial['etapeevolution'] = etapes_actives.first()
        else:
            # Si aucun poisson n'est sélectionné
            self.fields['etapeevolution'].queryset = EtapeEvolution.objects.none()


class MortaliteForm(forms.ModelForm):
    class Meta:
        model = Mortalite
        fields = ['poisson', 'mortalite', 'date_mortalite']
        widgets = {
    'poisson': forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'Nom du poisson',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'mortalite': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Nombre de mortalité',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'date_mortalite': forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}


class rationalimentaireForm(forms.ModelForm):
    class Meta:
        model = RationAlimentaire
        fields = ['poisson']
        widgets = {
    'poisson': forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'Lot de poissons',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    }

class SuiviCroissanceForm(forms.ModelForm):
    class Meta:
        model = SuiviCroissance
        fields = ['poisson', 'date_mesure', 'poids', 'commentaires']
        widgets = {

    'poisson': forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'Nom du bassin',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'poids': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'poids actuel',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'commentaires': forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': 'commentaires',
        'rows':3,
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'date_mesure': forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}
        
class PecheDeCalibrageForm(forms.ModelForm):
    class Meta:
        model = PecheDeCalibrage
        fields = ['poisson', 'date_peche', 'poids_moyen', 'quantite_peche', 'commentaires']
        widgets = {

    'poisson': forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'Nom du bassin',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'poids_moyen': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'poids moyen',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'quantite_peche': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Quantité pêchée',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'commentaires': forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': 'commentaires',
        'rows':3,
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'date_peche': forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}


class StockAlimentaireForm(forms.ModelForm):
    class Meta:
        model = Historique_stock
        fields = ['stock', 'quantite_ajoute', 'date_mise_a_jour']
        widgets = {

    'stock': forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'stock',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'quantite_ajoute': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Quantité',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'date_mise_a_jour': forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}
        
class DepenseForm(forms.ModelForm):
    fichiers = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Depense
        fields = ['sourcefine','categorie', 'montant', 'description', 'date_depense', 'fichiers']
        
        widgets = {
            'categorie': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Catégorie',
                'style': 'font-size: 20px; color: #043372; font-weight: bold;'
            }),
            'sourcefine': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'source de financement',
                'style': 'font-size: 20px; color: #043372; font-weight: bold;'
            }),
            'montant': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'montant',
                'style': 'font-size: 20px; color: #043372; font-weight: bold;'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Description',
                'rows': 3,
                'style': 'font-size: 20px; color: #043372; font-weight: bold;'
            }),
            'date_depense': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control', 
                'style': 'font-size: 20px; color: #043372; font-weight: bold;'
            }),
        }
    def clean(self):
        cleaned_data = super().clean()
        sourcefine = cleaned_data.get('sourcefine')
        montant_depense = cleaned_data.get('montant')

        if sourcefine and montant_depense:
            # Vérifier si le solde de la sourcefine est suffisant
            if sourcefine.solde < montant_depense:
                raise ValidationError("Le solde de la source de financement est insuffisant pour cette dépense.")

        return cleaned_data





        
class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['utilisateur', 'poste', 'date_embauche']
        widgets = {

    'utilisateur': forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'Utilisateur',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'poste': forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Fonction de l\'employé',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'date_embauche': forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}

        
class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['quantite_vendue','Poids', 'prix_vente', 'date_vente', 'client', 'commentaires']
        widgets = {

    'quantite_vendue': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'quantite vendue',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'prix_vente': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'prix de vente',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'Poids': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Poids',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'client': forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'client',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'commentaires': forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': 'commentaires',
        'rows': 3,
        'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
    }),
    'date_vente': forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}
        

class EtapeEvolutionForm(forms.ModelForm):
    class Meta:
        model = EtapeEvolution
        fields = ['poisson', 'stade_actuel', 'date_debut','date_fin','nombre_jour','status_actuel','couleur','commentaires','etat']
        widgets = {
            'poisson': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold; '  # Texte en gras
            }),
            'stade_actuel': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold; '  # Texte en gras
            }),
            'date_debut': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control', 
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;' 
                }),
            'date_fin': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control', 
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;' 
                }),
            'nombre_jour': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre de jour',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
            'status_actuel': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold; '  # Texte en gras
            }),
            'couleur': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'couleur',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
            'commentaires': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'commentaires',
                'rows': 3,
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
        }


class AlimentRecommandeForm(forms.ModelForm):
    class Meta:
        model = AlimentRecommande
        fields = ['espece', 'stade', 'aliment', 'quantite_recommandee','prix']
        
        widgets = {
            'espece': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold; '  # Texte en gras
            }),
            'stade': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold; '  # Texte en gras
            }),
            'aliment': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold; '  # Texte en gras
            }),
            'quantite_recommandee': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Quantite recommandée',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
            'prix': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Prix par gramme',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
            
        }


class AlimentForm(forms.ModelForm):
    class Meta:
        model = Aliment
        fields = ['nom', 'calibre', 'teneur_proteine', 'prix_par_kg', 'unite']
        
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom de l\'aliment',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
            'calibre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'calibre',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
            'teneur_proteine': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Teneur en proteine',
                'rows': 3,
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
            'prix_par_kg': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Prix par kilogramme',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
            'unite': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold; '  # Texte en gras
            })
        }

class NormeCroissanceForm(forms.ModelForm):
    class Meta:
        model = NormeCroissance
        fields = ['espece', 'stade', 'poids_min', 'poids_max', 'age_min', 'age_max']
        widgets = {
            'espece': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold; '  # Texte en gras
            }),
            'stade': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold; '  # Texte en gras
            }),
            'poids_min': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Poids mininal',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
            'poids_max': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Poids maximal',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
            'age_min': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'âge minimal',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
            'age_max': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': '',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
        }


class FichierModelForm(forms.ModelForm):
    fichier = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Fichier
        fields = ['nom', 'fichier']

        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du fichier',
            })
        }




class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['nom', 'contact']
        widgets = {

    'nom': forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'nom',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'contact': forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'contact',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

}



class BonDeCommandeForm(forms.ModelForm):
    ModeVente_CHOICES = [
        ('Bonchamp', 'Mode Bon Champ'),
        ('Livre', 'Mode Livraison'),
    ]
    TypePaiement_CHOICES = [
        ('solde', 'PAYE'),
        ('avance', 'Payer une avance'),
        ('aucun', 'Aucun paiement'),
    ]

    modevente = forms.ChoiceField(
        choices=ModeVente_CHOICES,
        label="Sélectionnez un mode de vente",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'font-size: 20px; color: #043372; font-weight: bold;',
        })
    )
    
    typepaiement = forms.ChoiceField(
        choices=TypePaiement_CHOICES,
        label="Sélectionnez un type de paiement",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'font-size: 20px; color: #043372; font-weight: bold;',
        })
    )
    class Meta:
        model = BonDeCommande
        fields = ['client','date_vente']

        widgets = {

    'client': forms.Select(attrs={
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'date_vente': forms.DateInput(attrs={
        'type': 'date',
        'class': '', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}

class LigneBonDeCommandeForm(forms.ModelForm):
    class Meta:
        model = LigneCommande
        fields = ['bande', 'quantite','prix_unitaire']
        widgets = {
    'bande': forms.Select(attrs={
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'quantite': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'quantite',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'prix_unitaire': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'prix_unitaire',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

}


class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['montant_paye', 'date_paiement']  # Champs éditables par l'utilisateur
        widgets = {

    'montant_paye': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'montant payé',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'date_paiement': forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}

# LigneBonDeCommandeFormSet = inlineformset_factory(
#     BonDeCommande, LigneCommande, form=LigneBonDeCommandeForm, extra=1, can_delete=True
# )


class BeneficeCibleForm(forms.Form):
    espece = forms.ModelChoiceField(
        queryset=EspecePoisson.objects.all(),
        label="Espèce de poisson",
        empty_label="Choisissez une espèce",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'font-size: 20px; color: #043372; font-weight: bold;'
        })
    )
    benefice_cible = forms.DecimalField(
        label="Bénéfice cible",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Bénéfice cible',
            'style': 'font-size: 20px; color: #043372; font-weight: bold;'
        })
    )
    prix_vente_par_kg = forms.DecimalField(
        label="Prix de vente par kg",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prix de vente par kg',
            'style': 'font-size: 20px; color: #043372; font-weight: bold;'
        })
    )
    taux_mortalite = forms.DecimalField(
        label="Taux de mortalité (%)",
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Taux de mortalité prévisionnel',
            'style': 'font-size: 20px; color: #043372; font-weight: bold;'
        })
    )
    duree_elevage = forms.IntegerField(
        label="Durée d'élevage (jours)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Durée de l\'élevage',
            'style': 'font-size: 20px; color: #043372; font-weight: bold;'
        })
    )

class VariablecibleForm(forms.Form):
    VARIABLE_CHOICES = [
        ('benef', 'Bénéfice cible'),
        ('invest', 'Investissement'),
        ('quant', 'Quantité'),
    ]
    
    variable_selection = forms.ChoiceField(choices=VARIABLE_CHOICES, label="Sélectionnez une variable")
    valeur_variable = forms.CharField(max_length=100, label="Entrez une valeur")



class Historique_sourcefineForm(forms.ModelForm):
    class Meta:
        model = Historique_Sourcefine
        fields = ['sourcefine', 'Montant']
        
        widgets = {
            'Sourcefine': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold; '  # Texte en gras
            }),
            'Montant': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Montant',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
            
        }

class SourcefineForm(forms.ModelForm):
    class Meta:
        model = Sourcefine
        fields = ['nom', 'solde','etat']
        
        widgets = {
                'nom': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'nom',
                'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
            }),

            'solde': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Montant',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;',  # Texte en gras
                # 'disabled': 'disabled'  # Rendre le champ inactif
            }),
'etat': forms.CheckboxInput(attrs={
                'class': 'form-check-input',  # Utilisez 'form-check-input' pour Bootstrap si nécessaire
                'style': 'width: 25px; height: 25px;',  # Ajustez la taille
                'title': 'Activer ou désactiver'  # Astuce au survol
            }),
            
        }


class DemandeReductionForm(forms.ModelForm):
    class Meta:
        model = demandeReduction
        fields = [
            'client', 'espece', 'ModeVente', 
            'quantite', 'poids', 'cout', 
            'taux_reduction', 'prix_unitaire_reduction', 
            'cout_reduction'
        ]
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'espece': forms.Select(attrs={'class': 'form-control'}),
            'ModeVente': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            'poids': forms.NumberInput(attrs={'class': 'form-control'}),
            'cout': forms.NumberInput(attrs={'class': 'form-control'}),
            'taux_reduction': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix_unitaire_reduction': forms.NumberInput(attrs={'class': 'form-control'}),
            'cout_reduction': forms.NumberInput(attrs={'class': 'form-control'}),
        }
