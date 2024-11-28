from django.apps import AppConfig
from django.conf import settings


from crafter.utils.settings_validator import validate_settings, SettingsValidationError


class CrafterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crafter'

    def ready(self):
        try:
            validate_settings()
            print(f"Using: {settings.CRAFTER_CHAT_ENGINE.upper()}")
        except SettingsValidationError as e:
            print(f"Settings validation error:\n{e}")
            print("Stopping the server automatically")
            exit(1)