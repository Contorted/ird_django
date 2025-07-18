from django.apps import AppConfig

class CommunicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'communications'
    
    def ready(self):
        import communications.signals  # Import signals when app is ready