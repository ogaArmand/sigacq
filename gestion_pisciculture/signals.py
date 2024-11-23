from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import *
from .views import *
from django.utils.timezone import now

register = template.Library()

@register.filter
def space_separated(value):
    try:
        value = int(value)
        return f"{value:,}".replace(",", " ")
    except (ValueError, TypeError):
        return value
    

@receiver(post_save, sender=Mortalite)
@receiver(post_delete, sender=Mortalite)
def update_nombre_poisson_dispo_taux_mortalite_reel(sender, instance, **kwargs):
    # Obtenez le poisson lié à l'enregistrement de mortalité
    poisson = instance.poisson

    # Utilisez la valeur initiale de nombre_alevins pour les calculs sans la modifier
    nombre_alevins_initial = poisson.nombre_alevins

    # Calcul de la mortalité totale pour ce poisson spécifique
    mortalite_totale = Mortalite.objects.filter(poisson=poisson).aggregate(total=Sum('mortalite'))['total'] or 0
    mortalite_totale = float(mortalite_totale)

    # Mise à jour du nombre de poissons disponibles (sans changer nombre_alevins)
    poisson.nombre_poisson_dispo = nombre_alevins_initial - int(mortalite_totale)

    # Calcul et mise à jour du taux de mortalité réel
    if nombre_alevins_initial > 0:
        poisson.taux_mortalite_reel = round((mortalite_totale / nombre_alevins_initial) * 100,2)
    else:
        poisson.taux_mortalite_reel = 0

    # Sauvegarde des modifications dans le modèle Poisson, sans toucher à `nombre_alevins`
    poisson.save()


# # Signal pour les dépenses
# @receiver(post_save, sender=Depense)
# def notify_depense_save(sender, instance, **kwargs):
#     msg = f"Nouvelle dépense enregistrée. Catégorie dépense : {instance.categorie}, Montant : {instance.montant} FCFA, Date : {instance.date_depense}."
#     send_sms(msg, "2250544169597")

# @receiver(post_save, sender=Vente)
# def notify_vente_save(sender, instance, **kwargs):
#     msg = f"Nouvelle vente enregistrée : Client : {instance.client}, Poids : {instance.Poids} kg, Prix : {instance.prix_vente} FCFA, Date : {instance.date_vente}."
#     send_sms(msg, "2250544169597")



# # Signal pour les dépenses
# @receiver(post_save, sender=Depense)
# def notify_depense_save(sender, instance,created, **kwargs):
#     # Calcul du total des dépenses pour le mois en cours
#     mois_courant = now().month
#     annee_courante = now().year
#     total_depenses = Depense.objects.filter(
#         date_depense__month=mois_courant, 
#         date_depense__year=annee_courante
#     ).aggregate(total=Sum('montant'))['total'] or 0

#     # Message SMS en fonction de la création ou modification
#     if created:
#         msg = (
#             f"Nouvelle dépense enregistrée.\n"
#             f"Catégorie : {instance.categorie}, Montant : {space_separated(instance.montant)} FCFA, "
#             f"Date : {instance.date_depense}.\n"
#             f"Total des dépenses du mois en cours : {space_separated(total_depenses)} FCFA."
#         )
#     else:
#         msg = (
#             f"Dépense modifiée.\n"
#             f"Catégorie : {instance.categorie}, Montant : {space_separated(instance.montant)} FCFA, "
#             f"Date : {instance.date_depense}.\n"
#             f"Total des dépenses du mois en cours : {space_separated(total_depenses)} FCFA."
#         )
    
#     # Envoi du message SMS
#     send_sms(msg)

# # Signal pour les ventes
# @receiver(post_save, sender=Vente)
# def notify_vente_save(sender, instance,created, **kwargs):
#     # Calcul du total des ventes pour le mois en cours
#     mois_courant = now().month
#     annee_courante = now().year
#     total_ventes = Vente.objects.filter(
#         date_vente__month=mois_courant, 
#         date_vente__year=annee_courante
#     ).aggregate(total=Sum('prix_vente'))['total'] or 0

#     # Message SMS en fonction de la création ou modification
#     if created:
#         msg = (
#             f"Nouvelle vente enregistrée.\n"
#             f"Client : {instance.client}, Poids : {instance.Poids} kg, "
#             f"Prix : {space_separated(instance.prix_vente)} FCFA, Date : {instance.date_vente}.\n"
#             f"Total des ventes du mois en cours : {space_separated(total_ventes)} FCFA."
#         )
#     else:
#         msg = (
#             f"Vente modifiée.\n"
#             f"Client : {instance.client}, Poids : {instance.Poids} kg, "
#             f"Prix : {space_separated(instance.prix_vente)} FCFA, Date : {instance.date_vente}.\n"
#             f"Total des ventes du mois en cours : {space_separated(total_ventes)} FCFA."
#         )
    
#     # Envoi du message SMS
#     send_sms(msg)


# @receiver(post_save, sender=Depense)
# def check_seuil_depense(sender, instance, **kwargs):
#     # Obtenir le seuil actuel de la configuration
#     config = Configuration.objects.first()
#     if not config:
#         return  # Si aucune configuration n'existe, ne rien faire

#     seuil = config.seuil_depense

#     # Calculer le total des dépenses pour le mois en cours
#     mois_courant = now().month
#     annee_courante = now().year
#     total_depenses = Depense.objects.filter(
#         date_depense__month=mois_courant, 
#         date_depense__year=annee_courante
#     ).aggregate(total=Sum('montant'))['total'] or 0
    
#     # Vérifier si le seuil est atteint ou dépassé
#     if total_depenses >= seuil:
#         msg = (
#             f"Attention : Le seuil des dépenses a été atteint !\n"
#             f"Total actuel des dépenses : {total_depenses} FCFA (Seuil : {seuil} FCFA)."
#         )
#         send_sms(msg)  # Remplacez par le numéro du patron