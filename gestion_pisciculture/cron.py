# from django_cron import CronJobBase, Schedule
# from .models import Poisson, SuiviAlimentaire, RationAlimentaire
# from datetime import date
# import logging
# logger = logging.getLogger(__name__)

# class SuiviAlimentaireCronJob(CronJobBase):
#     # Exécution quotidienne
#     RUN_EVERY_MINS = 1  

#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'app.suivi_alimentaire_cron_job'  # Code unique
#     print('debut de la tâche')
#     def do(self):
#         print("Cron Job exécuté")
#         """
#         Génère automatiquement un SuiviAlimentaire pour chaque poisson chaque jour.
#         """
#         poissons = Poisson.objects.all()
#         for poisson in poissons:
#             try:
#                 ration_recom = RationAlimentaire.objects.get(poisson=poisson)
#                 print(f"Ration pour {poisson} trouvée : {ration_recom.quantite}")
#                 # Créer une nouvelle entrée de suivi alimentaire
#                 SuiviAlimentaire.objects.create(
#                     poisson=poisson,
#                     rationalimentaire_recom=ration_recom.quantite,
#                     rationalimentaire_donnee=0.0,
#                     rationalimentaire_ecart=ration_recom.quantite,
#                     date_alimentation_reel=date.today(),
#                 )
#                 logger.info(f"Suivi alimentaire créé pour le poisson : {poisson}")
#                 print(f"Suivi alimentaire créé pour le poisson : {poisson}")
#             except RationAlimentaire.DoesNotExist:
#                 logger.warning(f"Aucune ration recommandée trouvée pour le poisson : {poisson}")
#                 print(f"Aucune ration recommandée trouvée pour le poisson : {poisson}")
