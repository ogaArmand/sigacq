# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery

# # Définir le module de configuration Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pisciculture.settings')

# # Créer l'application Celery
# app = Celery('pisciculture')

# # Charger la configuration depuis les paramètres de Django
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Charger les tâches automatiquement depuis tous les apps installés
# app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
