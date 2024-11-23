from django import forms
from .models import *
from django.forms import inlineformset_factory

class BassinForm(forms.ModelForm):
    class Meta:
        model = Bassin
        fields = ['nom', 'capacite', 'temperature_courante', 'description']
        widgets = {
    'nom': forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Nom du bassin',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'capacite': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Capacité',
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


class PoissonForm(forms.ModelForm):
    class Meta:
        model = Poisson
        fields = ['espece', 'bassin', 'date_introduction', 'poids_initial', 'poids_actuel', 'nombre_alevins', 'taux_mortalite']
        widgets = {
    'espece': forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'Nom du bassin',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'bassin': forms.Select(attrs={
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'poids_initial': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'poids initial',
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
        'placeholder': 'poids actuel',
        'rows':3,
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'date_mesure': forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}



class StockAlimentaireForm(forms.ModelForm):
    class Meta:
        model = StockAlimentaire
        fields = ['aliment', 'quantite_disponible', 'date_mise_a_jour']
        widgets = {

    'aliment': forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'aliment',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'quantite_disponible': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'quantite disponible',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'date_mise_a_jour': forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}
        
class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = ['categorie', 'montant', 'description','date_depense']
        widgets = {

    'categorie': forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'categorie',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'montant': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'montant',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
    'description': forms.Textarea(attrs={
        'class': 'form-control', 
        'placeholder': 'description',
        'rows': 3,
        'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
    }),
    'date_depense': forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}
        
class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['utilisateur', 'poste', 'date_embauche']
        widgets = {

    'utilisateur': forms.Select(attrs={
        'class': 'form-control', 
        'placeholder': 'aliment',
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),

    'poste': forms.NumberInput(attrs={
        'class': 'form-control', 
        'placeholder': 'quantite disponible',
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
        fields = ['nom', 'type_aliment', 'composition', 'prix_par_kg', 'unite']
        
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom de l\'aliment',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
            'type_aliment': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Type d\'aliment',
                'style': 'font-size: 20px;' 'color: #043372;' 'font-weight: bold;'  # Texte en gras
            }),
            'composition': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Composition nutritionnelle',
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
        model = Client
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
    class Meta:
        model = BonDeCommande
        fields = ['client']
        widgets = {
    'client': forms.Select(attrs={
        'class': 'form-control', 
        'style': 'font-size: 20px;' 'color: #043372; font-weight: bold;'  # Agrandir la taille du texte
    }),
}

class LigneBonDeCommandeForm(forms.ModelForm):
    class Meta:
        model = LigneCommande
        fields = ['poisson', 'quantite','prix_unitaire']
        widgets = {
    'poisson': forms.Select(attrs={
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