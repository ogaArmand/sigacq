from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models import F
from datetime import timedelta
import base64
import zlib  # Pour la compression
from cryptography.fernet import Fernet  # Pour le chiffrement
from django.utils import timezone
import datetime
from django.utils.crypto import get_random_string

class superficie(models.Model):
    superficie = models.CharField(max_length=100)
    capacite = models.FloatField()  # Nombre de poissons possible
    profondeur = models.FloatField(default=0)  # Profondeur en mètres
    capacite_eau = models.FloatField(default=0)  # Capacité en litres
    unite = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Calculer la capacité en eau en litres
        if self.profondeur > 0:
            # Conversion de la superficie en m² si elle est dans une autre unité
            try:
                superficie_en_m2 = float(self.superficie)  # Assurer que la superficie est un float
            except ValueError:
                # Gérer le cas où la superficie n'est pas un nombre directement
                superficie_en_m2 = 0
            
            # Calcul du volume d'eau en m³
            volume_m3 = superficie_en_m2 * self.profondeur

            # Conversion en litres (1 m³ = 1000 litres)
            self.capacite_eau = volume_m3
        else:
            self.capacite_eau = 0  # Si la profondeur est zéro ou non valide, la capacité est zéro
        
        # Appel du super() pour conserver le comportement par défaut de save()
        super(superficie, self).save(*args, **kwargs)

    def __str__(self):
        return self.superficie


class Bassin(models.Model):
    nom = models.CharField(max_length=100)
    superficie = models.ForeignKey(superficie, on_delete=models.CASCADE, default=1)
    contenu_reel = models.FloatField(default=0)
    ecart_contenu = models.FloatField(default=0)
    capacite_eau_reel = models.FloatField(default=0)
    ecart_capacite_eau = models.FloatField(default=0)
    temperature_courante = models.FloatField(null=True)  # Température actuelle de l'eau
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculer l'écart entre la capacité de la superficie et le contenu réel
        self.ecart_contenu = self.contenu_reel - self.superficie.capacite
        self.ecart_capacite_eau = self.capacite_eau_reel - self.superficie.capacite_eau
        super(Bassin, self).save(*args, **kwargs)

    def __str__(self):
        return self.nom

    # Méthode pour renvoyer l'interprétation de l'écart en pourcentage
    def interpretation_ecart(self):
        if self.superficie.capacite == 0:  # Éviter la division par zéro
            return "Capacité de superficie n'est pas définie."
        
        # Calcul du pourcentage d'écart
        pourcentage_ecart = (self.ecart_contenu / self.superficie.capacite) * 100

        if pourcentage_ecart <= -5:
            return "Soupleupement. Vous avez encore la possibilité d'ajouter d'autres poissons"
        elif pourcentage_ecart > -5 and pourcentage_ecart <= 5:
            return "État normal."
        elif pourcentage_ecart > 5 and pourcentage_ecart <= 10:
            return "État acceptable."
        else:
            return "Surpeuplement. Suggestion : Reduire le nombre de poissons pour optimiser leur croissance"
    # Méthode pour renvoyer l'interprétation de l'écart en pourcentage
    def interpretation_ecart_eau(self):
        if self.superficie.capacite_eau == 0:  # Éviter la division par zéro
            return "Capacité de superficie n'est pas définie."
        
        # Calcul du pourcentage d'écart
        pourcentage_ecart = (self.ecart_capacite_eau / self.superficie.capacite_eau) * 100

        if pourcentage_ecart <= -5:
            return "Besoin urgent en eau"
        elif pourcentage_ecart > -5 and pourcentage_ecart <= 5:
            return "Bonne quantité d'eau"
        else:
            return "Quantité d'eau beaucoup trop élevée"



class Souche(models.Model):
    souche = models.CharField(max_length=100)
    def __str__(self):
        return self.souche
    
class EspecePoisson(models.Model):
    nom = models.CharField(max_length=100)
    souche = models.ForeignKey(Souche, on_delete=models.CASCADE,default=1)
    indice_conversion = models.FloatField(default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom
    

class Stade(models.Model):
    stade = models.CharField(max_length=100)
    def __str__(self):
        return f"Stade de {self.stade}"

class NormeCroissance(models.Model):
    espece = models.ForeignKey(EspecePoisson, on_delete=models.CASCADE)  # Espèce de poisson
    stade = models.ForeignKey(Stade, on_delete=models.CASCADE,default=1)  # Espèce de poisson
    poids_min = models.FloatField()  # Poids minimum attendu (en grammes)
    poids_max = models.FloatField()  # Poids maximum attendu (en grammes)
    age_min = models.IntegerField()  # Âge minimum (en jours)
    age_max = models.IntegerField()  # Âge maximum (en jours)

    def __str__(self):
        return f"Norme de croissance pour {self.espece.nom} au stade {self.stade}"
    
class Poisson(models.Model):
    espece = models.ForeignKey(EspecePoisson, on_delete=models.CASCADE)
    bassin = models.ForeignKey(Bassin, on_delete=models.CASCADE)
    date_introduction = models.DateField()
    poids_initial = models.FloatField()  # Poids moyen des alevins à l'introduction
    poids_actuel = models.FloatField()
    nombre_alevins = models.IntegerField()  # Nombre d'alevins dans le lot
    taux_mortalite = models.FloatField(default=0.0)  # Taux de mortalité prévu ou observé
    nombre_poisson_dispo = models.IntegerField(default=0)
    taux_mortalite_reel = models.FloatField(default=0.0)
    def __str__(self):
        return f"Lot de {self.nombre_alevins} alevins de {self.espece.nom} dans {self.bassin.nom}"
    
    def update_stock(self):
        # Calcul de la mortalité totale pour ce lot de poissons
        mortalite_totale = Mortalite.objects.filter(poisson=self).aggregate(total=Sum('mortalite'))['total'] or 0
        mortalite_totale = float(mortalite_totale)  # Assurez-vous que c'est un float

        # Calcul de la quantité totale vendue pour ce lot de poissons
        quantite_vendue = LigneCommande.objects.filter(poisson=self).aggregate(total=Sum('quantite'))['total'] or 0
        quantite_vendue = int(quantite_vendue)  # Assurez-vous que c'est un entier

        # Mise à jour du nombre de poissons disponibles
        self.nombre_poisson_dispo = self.nombre_alevins - int(mortalite_totale) - quantite_vendue

        # Calcul et mise à jour du taux de mortalité réel
        if self.nombre_alevins > 0:
            self.taux_mortalite_reel = (mortalite_totale / self.nombre_alevins) * 100
        else:
            self.taux_mortalite_reel = 0

        # Sauvegarde de l'instance avec les valeurs mises à jour
        self.save()


class Aliment(models.Model):
    UNITE_CHOICES = [
        ('kg', 'Kilogramme'),
        ('g', 'Gramme'),
        ('L', 'Litre'),
    ]
    
    nom = models.CharField(max_length=100)
    calibre = models.CharField(max_length=100,null=True)  # Granulé, insectes, etc.
    teneur_proteine = models.CharField(max_length=100,null=True)  # Granulé, insectes, etc.
    prix_par_kg = models.DecimalField(max_digits=10, decimal_places=2)
    unite = models.CharField(max_length=5, choices=UNITE_CHOICES, default='g')  # Unité de mesure

    def __str__(self):
        return f"{self.nom} ({self.unite})"


class RationAlimentaire(models.Model):
    poisson = models.ForeignKey(Poisson, on_delete=models.CASCADE)
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    quantite = models.FloatField(null=True)  # Quantité donnée en grammes
    cout_total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    date_distrib = models.DateField()

    def __str__(self):
        return f"{self.quantite}g de {self.aliment.nom} à {self.poisson.espece.nom} le {self.date_distrib}"

class Mortalite(models.Model):
    poisson = models.ForeignKey(Poisson, on_delete=models.CASCADE)
    mortalite = models.FloatField(null=True)  # Poids à la date de mesure
    date_mortalite = models.DateField()
    def __str__(self):
        return self.poisson.espece.nom

class SuiviCroissance(models.Model):
    poisson = models.ForeignKey(Poisson, on_delete=models.CASCADE)
    date_mesure = models.DateField()
    poids = models.FloatField()  # Poids à la date de mesure
    poids_attendu_min = models.FloatField(default=0.0)  # Poids min attendu
    poids_attendu_max = models.FloatField(default=0.0)  # Poids max attendu
    commentaires = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Suivi du {self.date_mesure} pour {self.poisson.espece.nom}"

    def verifier_conformite(self):
        # Récupérer l'étape d'évolution actuelle du poisson
        etape_actuelle = EtapeEvolution.objects.filter(poisson=self.poisson).order_by('-date_debut').first()
        
        # Vérifier s'il existe une norme pour cette espèce et ce stade
        norme = NormeCroissance.objects.filter(espece=self.poisson.espece, stade=etape_actuelle.stade_actuel).first()

        if norme:
            # Calculer l'âge du poisson en jours depuis sa date d'introduction
            age_poisson = (self.date_mesure - self.poisson.date_introduction).days


            self.poids_attendu_min = norme.poids_min
            self.poids_attendu_max = norme.poids_max
            self.save()
            # Comparer avec la norme de croissance
            if norme.poids_min <= self.poids <= norme.poids_max and norme.age_min <= age_poisson <= norme.age_max:
                return "Croissance conforme"
            else:
                return "Croissance non conforme"
        return "Norme de croissance non définie"

    def save(self, *args, **kwargs):
        # Mettre à jour les commentaires en fonction de la conformité
        self.commentaires = self.verifier_conformite()

        # Sauvegarder la nouvelle mesure de croissance
        super(SuiviCroissance, self).save(*args, **kwargs)

        # Mettre à jour le poids actuel du poisson si c'est la dernière mesure
        derniere_mesure = SuiviCroissance.objects.filter(poisson=self.poisson).order_by('-date_mesure').first()

        if derniere_mesure and derniere_mesure == self:
            # Si c'est la dernière mesure, mettre à jour le poids actuel du poisson
            self.poisson.poids_actuel = self.poids
            self.poisson.save()



# class NormeCroissance(models.Model):
#     norme = models.CharField(max_length=100)
#     poids = models.FloatField()  # Poids de référence
#     couleur = models.CharField(max_length=100)



class Employe(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    poste = models.CharField(max_length=100)  # Poste dans l'entreprise (ex: gestionnaire)
    date_embauche = models.DateField()

    def __str__(self):
        return f"{self.utilisateur.first_name} {self.utilisateur.last_name}"




class Facture(models.Model):
    client = models.CharField(max_length=100)
    date_vente = models.DateField()
    poisson = models.ForeignKey(Poisson, on_delete=models.CASCADE)
    quantite_vendue = models.FloatField(default=0)  # Quantité en kg
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Facture du {self.date_vente} pour {self.client}"


    
class EtapeEvolution(models.Model):
    # STADES = [
    #     ('lavaire', 'lavaire'),# 0.01 g à 0.4 g
    #     ('Alevin', 'Alevin'), # 28 jours après (0.5 g à 0.9 g)
    #     ('Juvénil', 'Juvénil'), # 1 g à 25 g
    #     ('pre-grossissement', 'Pré-grossissement'),
    #     ('grossissement', 'Grossissement'),
    #     ('commercialisation', 'Commercialisation'),
    # ]
    STATUS = [
        ('mauvaise', 'mauvaise'),
        ('moyenne', 'moyenne'),
        ('bonne', 'bonne'),
    ]
    poisson = models.ForeignKey(Poisson, on_delete=models.CASCADE)
    stade_actuel = models.ForeignKey(Stade, on_delete=models.CASCADE,default=1)
    # stade_actuel = models.CharField(max_length=20, choices=STADES)
    date_debut = models.DateField()  # Date de début de cette étape
    date_fin = models.DateField(blank=True, null=True)  # Date de fin (pour les étapes terminées)
    nombre_jour = models.IntegerField(null=True)
    status_actuel = models.CharField(max_length=20, choices=STATUS, null=True)
    etat = models.BooleanField(default=0) # stade en cours
    couleur = models.CharField(max_length=20, null=True)
    commentaires = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.poisson.espece.nom} - {self.stade_actuel} (Début: {self.date_debut})"

    # def save(self, *args, **kwargs):
    #     # Appeler la méthode save de base pour enregistrer la première étape
    #     super(EtapeEvolution, self).save(*args, **kwargs)

    #     # Si on enregistre une étape de type 'pré-grossissement'
    #     if self.stade_actuel == 'pre-grossissement':
    #         # Assurer que les étapes suivantes n'existent pas déjà pour ce poisson
    #         if not EtapeEvolution.objects.filter(poisson=self.poisson, stade_actuel='grossissement').exists():
                
    #             # Calculer la date de fin pour 'pré-grossissement'
    #             if not self.date_fin:
    #                 self.date_fin = self.date_debut + timedelta(days=self.nombre_jour)
    #                 self.save()  # Sauvegarder à nouveau pour enregistrer la date de fin

    #             # Créer automatiquement l'étape 'grossissement'
    #             date_debut_grossissement = self.date_fin + timedelta(days=1)
    #             etape_grossissement = EtapeEvolution.objects.create(
    #                 poisson=self.poisson,
    #                 stade_actuel='grossissement',
    #                 etat = 0,
    #                 date_debut=date_debut_grossissement,
    #                 nombre_jour=60,  # Nombre de jours pour le grossissement
    #             )

    #             # Créer automatiquement l'étape 'commercialisation'
    #             date_debut_commercialisation = etape_grossissement.date_debut + timedelta(days=etape_grossissement.nombre_jour)
    #             EtapeEvolution.objects.create(
    #                 poisson=self.poisson,
    #                 stade_actuel='commercialisation',
    #                 etat = 0,
    #                 date_debut=date_debut_commercialisation,
    #                 nombre_jour=30,  # Nombre de jours pour la commercialisation
    #             )



class AlimentRecommande(models.Model):
    espece = models.ForeignKey(EspecePoisson, on_delete=models.CASCADE)  # Espèce de poisson
    stade = models.ForeignKey(Stade, on_delete=models.CASCADE,default=1)  # Espèce de poisson
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)  # Aliment recommandé
    quantite_recommandee = models.FloatField()  # Quantité recommandée en grammes par poisson
    prix = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Prix total calculé

    def __str__(self):
        return f"{self.aliment.nom} recommandé pour {self.espece.nom} au stade {self.stade}"
    
    def calculer_cout_total(self, nombre_poissons):
        # Convertir la quantité recommandée en kilogrammes (supposons que la quantité recommandée est en grammes)
        quantite_g = self.quantite_recommandee
        prix_g = int(self.aliment.prix_par_kg)/1000.0

        # Calculer le coût total pour tous les poissons
        cout_total = quantite_g * nombre_poissons * prix_g

        return cout_total


class StockAlimentaire(models.Model):
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    quantite_disponible = models.FloatField(null=True)  # Quantité en kg
    date_mise_a_jour = models.DateField()

    def __str__(self):
        return f"{self.quantite_disponible}kg de {self.aliment.nom} en stock"

class alimentation(models.Model):
    ration_recommande = models.ForeignKey(RationAlimentaire, on_delete=models.CASCADE)

    
class Depense(models.Model):
    CATEGORIES = [
        ('alimentation', 'Alimentation'),
        ('soin', 'Soins'),
        ('infrastructure', 'Infrastructure'),
        ('autre', 'Autre'),
    ]
    categorie = models.CharField(max_length=20, choices=CATEGORIES)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date_depense = models.DateField()

    def __str__(self):
        return f"{self.categorie} - {self.montant} FCFA le {self.date_depense}"


class FichierDepense(models.Model):
    depense = models.ForeignKey(Depense, related_name='fichiers', on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='fichiers_depense/')


class Prevision(models.Model):
    bénéfice_cible = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente_kg = models.DecimalField(max_digits=10, decimal_places=2)
    taux_mortalite = models.FloatField()  # Pourcentage de mortalité
    duree_elevage = models.IntegerField()  # Durée en jours
    autres_depenses = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Infrastructures, énergie, etc.

    def __str__(self):
        return f"Prévisions pour un bénéfice cible de {self.bénéfice_cible}FCFA"



# class Fichier(models.Model):
#     nom = models.CharField(max_length=255)  # Nom du fichier
#     fichier_base64 = models.TextField()  # Données encodées en base64

#     def __str__(self):
#         return self.nom

#     # Méthode pour encoder et sauvegarder un fichier (directement depuis un fichier en mémoire)
#     def encoder_et_sauvegarder(self, fichier_obj):
#         fichier_binaire = fichier_obj.read()  # Lecture du fichier téléchargé
#         self.fichier_base64 = base64.b64encode(fichier_binaire).decode('utf-8')
#         self.save()

#     # Méthode pour décoder et récupérer le fichier
#     def decoder_et_sauvegarder(self, output_path):
#         fichier_decode = base64.b64decode(self.fichier_base64)
#         with open(output_path, "wb") as file:
#             file.write(fichier_decode)



# class Fichier(models.Model):
#     nom = models.CharField(max_length=255)  # Nom du fichier
#     extension = models.CharField(max_length=10,default='pdf')  # Extension du fichier (par exemple, 'pdf', 'png')
#     fichier_base64 = models.TextField(default='')  # Données encodées en base64

#     def __str__(self):
#         return f"{self.nom}.{self.extension}"

#     def encoder_et_sauvegarder(self, fichier_obj):
#         fichier_binaire = fichier_obj.read()  # Lecture du fichier téléchargé
#         self.nom = fichier_obj.name.split('/')[-1]  # Récupérer le nom du fichier
#         self.extension = fichier_obj.name.split('.')[-1]  # Extraire l'extension du fichier
#         self.fichier_base64 = base64.b64encode(fichier_binaire).decode('utf-8')
#         self.save()

#     def decoder_et_sauvegarder(self, output_path):
#         """
#         Décode les données base64 et sauvegarde le fichier sur le disque avec l'extension appropriée.
#         """
#         fichier_decode = base64.b64decode(self.fichier_base64)
#         with open(output_path, "wb") as file:
#             file.write(fichier_decode)


class Fichier(models.Model):
    nom = models.CharField(max_length=255)  # Nom du fichier
    fichier_base64 = models.TextField()  # Données encodées en base64 (compressées et chiffrées)
    extension = models.CharField(max_length=10)  # Extension du fichier

    def __str__(self):
        return self.nom

    # Méthode pour encoder, compresser et chiffrer un fichier
    def encoder_et_sauvegarder(self, fichier_obj):
        fichier_binaire = fichier_obj.read()  # Lecture du fichier téléchargé
        self.nom = fichier_obj.name.split('/')[-1]  # Récupérer le nom du fichier
        self.extension = fichier_obj.name.split('.')[-1]  # Extraire l'extension

        # Compression des données binaires
        fichier_compresse = zlib.compress(fichier_binaire)

        # Chiffrement des données compressées
        key = Fernet.generate_key()  # Génère une clé de chiffrement (à stocker quelque part en toute sécurité)
        cipher_suite = Fernet(key)
        fichier_chiffre = cipher_suite.encrypt(fichier_compresse)

        # Encoder en base64 pour stockage
        self.fichier_base64 = base64.b64encode(fichier_chiffre).decode('utf-8')
        self.save()

    # Méthode pour décompresser, déchiffrer et récupérer le fichier
    def decoder_et_recuperer(self):
        # Décoder les données base64
        fichier_chiffre = base64.b64decode(self.fichier_base64)

        # Clé de déchiffrement (à récupérer depuis là où elle est stockée)
        key = Fernet.generate_key()  # Ceci est un exemple. Normalement, tu dois récupérer la même clé utilisée pour le chiffrement
        cipher_suite = Fernet(key)

        # Déchiffrer les données
        fichier_compresse = cipher_suite.decrypt(fichier_chiffre)

        # Décompresser les données
        fichier_binaire = zlib.decompress(fichier_compresse)

        return fichier_binaire



class Client(models.Model):
    nom = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)

    def __str__(self):
        return self.nom



class BonDeCommande(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    date_commande = models.DateField(auto_now_add=True)
    date_vente = models.DateField(null=True)
    ref_bon = models.CharField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return f"Commande {self.ref_bon} de {self.client.nom}"

    def save(self, *args, **kwargs):
        # Si ref_bon n'existe pas, on le génère
        if not self.ref_bon:
            today = datetime.date.today().strftime('%Y%m%d')
            new_ref_num = 1  # Initialiser le numéro de la commande

            # Boucle pour trouver une référence unique
            while True:
                new_ref_bon = f"BC-{today}-{new_ref_num:04d}"
                if not BonDeCommande.objects.filter(ref_bon=new_ref_bon).exists():
                    self.ref_bon = new_ref_bon
                    break
                new_ref_num += 1  # Incrémente le numéro si la référence existe déjà

        super(BonDeCommande, self).save(*args, **kwargs)

# class BonDeCommande(models.Model):
#     client = models.ForeignKey(Client, on_delete=models.CASCADE)
#     date_commande = models.DateField(auto_now_add=True)
#     ref_bon = models.CharField(max_length=100, unique=True, blank=True)

#     def save(self, *args, **kwargs):
#         # Appel de la méthode save() originale pour que `date_commande` soit défini
#         if not self.ref_bon:
#             super().save(*args, **kwargs)  # Sauvegarder d'abord pour avoir `date_commande`

#             # Générer ref_bon après que date_commande soit défini
#             self.ref_bon = self.generate_unique_ref_bon()
#             kwargs['force_insert'] = False  # Empêcher la création d'un nouvel enregistrement
#         super().save(*args, **kwargs)

#     def generate_unique_ref_bon(self):
#         # Génère un numéro unique de bon de commande
#         ref_bon = f"BC-{self.date_commande.strftime('%Y%m%d')}-{get_random_string(6)}"
        
#         # Vérifie que ref_bon n'existe pas déjà
#         while BonDeCommande.objects.filter(ref_bon=ref_bon).exists():
#             ref_bon = f"BC-{self.date_commande.strftime('%Y%m%d')}-{get_random_string(6)}"
        
#         return ref_bon

#     def __str__(self):
#         return f"Commande {self.ref_bon} de {self.client.nom}"




class Vente(models.Model):
    bon_de_commande = models.ForeignKey(BonDeCommande, on_delete=models.CASCADE,null=True,blank=True)
    quantite_vendue = models.IntegerField(default=0)  # Quantité vendue en nombre d'alevins ou poissons
    Poids = models.DecimalField(max_digits=10, decimal_places=2,default=0) 
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)  # Prix total de la vente
    date_vente = models.DateField()
    client = models.CharField(max_length=100)
    commentaires = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Vente à {self.client}"
    

class LigneCommande(models.Model):
    bon_de_commande = models.ForeignKey(BonDeCommande, related_name='lignes', on_delete=models.CASCADE)
    poisson = models.ForeignKey(Poisson, on_delete=models.CASCADE)
    poids = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.DecimalField(max_digits=10, decimal_places=2)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    sous_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantite} {self.poisson.espece.nom}"
    
    def save(self, *args, **kwargs):
        # Vérifier si c'est une nouvelle vente
        if self.pk is None:  # Si l'objet est nouveau (ajout de vente)
            if self.poisson.nombre_poisson_dispo >= self.quantite:
                # Mise à jour du nombre d'alevins restant
                self.poisson.nombre_poisson_dispo = F('nombre_poisson_dispo') - self.quantite
                self.poisson.save()
            else:
                raise ValueError("La quantité d'alevins vendue dépasse le nombre disponible.")
        super().save(*args, **kwargs)  # Appel de la méthode save() originale



class Configuration(models.Model):
    seuil_depense = models.DecimalField(
        max_digits=12, decimal_places=2, 
        default=1000000,  # Par défaut, 1 000 000 FCFA
        help_text="Seuil total des dépenses pour déclencher une notification SMS."
    )

    def __str__(self):
        return f"Configuration: Seuil {self.seuil_depense} FCFA"
