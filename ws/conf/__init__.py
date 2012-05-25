from django.conf import settings, global_settings

from ws.conf import default_settings


def load_settings():
    for key, value in default_settings.__dict__.items():
        if not key.startswith('_'):
            global_setting = getattr(global_settings, key, None)
            setting = getattr(settings, key, None)
            if setting is None or setting == global_setting:
                setattr(settings, key, value)
    return settings
