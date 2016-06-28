from django.conf import settings


SETTINGS_KEY = 'ONESKY_CONFIG'
DEFAULTS = {
    'BASE_URL': 'https://platform.api.onesky.io/1/',
    'PUBLIC_KEY': None,
    'PRIVATE_KEY': None,
    'PO_TRANSLATE_PROJECT': None,
    'ENABLED': True
}


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
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        setattr(self, attr, val)
        return val


USER_SETTINGS = getattr(settings, SETTINGS_KEY, None)
app_settings = AppSettings(USER_SETTINGS, DEFAULTS)
