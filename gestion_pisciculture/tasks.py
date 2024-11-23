from celery import shared_task
from gestion_pisciculture.models import SuiviCroissance
from datetime import date

@shared_task
def mettre_a_jour_suivi_croissance():
    suivis_croissance = SuiviCroissance.objects.filter(date_mesure=date.today())
    for suivi in suivis_croissance:
        suivi.commentaires = suivi.verifier_conformite()
        suivi.save()
    return f'Mise à jour effectuée pour {suivis_croissance.count()} entrées.'
