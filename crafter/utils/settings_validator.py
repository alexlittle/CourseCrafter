from django.conf import settings

class SettingsValidationError(Exception):
    pass

def validate_settings():

    # Required settings and their validation criteria
    if not isinstance(settings.CRAFTER_CHAT_ENGINE, str) or settings.CRAFTER_CHAT_ENGINE not in ["openai", "ollama", "google-genai"]:
        raise SettingsValidationError(f"Please set a valid CRAFTER_CHAT_ENGINE (openai/ollama/google-genai)")

    if settings.CRAFTER_CHAT_ENGINE == "openai" and (not isinstance(settings.OPENAI_API_KEY, str) or len(settings.OPENAI_API_KEY) < 10):
        raise SettingsValidationError(f"To use openai please set an OPENAI_API_KEY")

    if settings.CRAFTER_CHAT_ENGINE == "google-genai" and (not isinstance(settings.GOOGLE_GEN_AI_API_KEY, str) or len(settings.GOOGLE_GEN_AI_API_KEY) < 10):
        raise SettingsValidationError(f"To use google-genai please set an GOOGLE_GEN_AI_API_KEY")

    if not isinstance(settings.CRAFTER_CHAT_ENGINE_MODEL, str) or len(settings.CRAFTER_CHAT_ENGINE_MODEL) < 5:
        raise SettingsValidationError(f"Please set a CRAFTER_CHAT_ENGINE_MODEL")
