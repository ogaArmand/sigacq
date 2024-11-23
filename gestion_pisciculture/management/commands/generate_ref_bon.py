from django.core.management.base import BaseCommand
from gestion_pisciculture.models import BonDeCommande
import datetime

class Command(BaseCommand):
    help = 'Génère des références ref_bon pour les enregistrements existants sans référence'

    def handle(self, *args, **kwargs):
        today = datetime.date.today().strftime('%Y%m%d')
        commandes = BonDeCommande.objects.filter(ref_bon__isnull=True)

        for index, commande in enumerate(commandes, start=1):
            new_ref_num = 1

            while True:
                new_ref_bon = f"BC-{today}-{new_ref_num:04d}"
                if not BonDeCommande.objects.filter(ref_bon=new_ref_bon).exists():
                    commande.ref_bon = new_ref_bon
                    commande.save()
                    break
                new_ref_num += 1

            self.stdout.write(self.style.SUCCESS(f"Référence générée pour la commande {commande.id}: {commande.ref_bon}"))

