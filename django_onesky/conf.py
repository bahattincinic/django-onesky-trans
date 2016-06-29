from django.conf import settings

try:
    # Available in Python 3.1+
    import importlib
except ImportError:
    # Will be removed in Django 1.9
    from django.utils import importlib


SETTINGS_KEY = 'ONESKY_CONFIG'
DEFAULTS = {
    'BASE_URL': 'https://platform.api.onesky.io/1/',
    'PUBLIC_KEY': None,
    'PRIVATE_KEY': None,
    'PROJECT_ID': None,
    'ENABLED': True,
    'MAKE_MESSAGES_PROCESS_CLASS': (
        'django_onesky.process_messages.MakeMessagesProcess'),
    'COMPILE_MESSAGES_PROCESS_CLASS': (
        'django_onesky.process_messages.CompileMessagesProcess')
}

IMPORT_STRINGS = (
    'MAKE_MESSAGES_PROCESS_CLASS',
    'COMPILE_MESSAGES_PROCESS_CLASS'
)


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (
            val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class AppSettings(object):
    """
    A settings object, that allows App settings to be accessed as properties.
    For example:

        from django_onesky.conf import app_settings
        print(app_settings.BASE_URL)
    """

    def __init__(self, user_settings=None, defaults=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or {}

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid APP setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        if attr in IMPORT_STRINGS:
            val = import_from_string(val, attr)

        # Cache the result
        setattr(self, attr, val)
        return val


USER_SETTINGS = getattr(settings, SETTINGS_KEY, None)
app_settings = AppSettings(USER_SETTINGS, DEFAULTS)
