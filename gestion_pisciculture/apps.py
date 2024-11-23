from django.apps import AppConfig


class GestionPiscicultureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_pisciculture'
    def ready(self):
        import gestion_pisciculture.signals  # Importer les signaux pour les enregistrer




