from django.conf import settings as base_settings


SETTINGS_KEY = 'ONESKY_CONFIG'
DEFAULTS = {
    'BASE_URL': 'https://platform.api.onesky.io/1/',
    'PUBLIC_KEY': None,
    'PRIVATE_KEY': None,
    'PO_TRANSLATE_PROJECT': None,
    'ENABLED': True,
    'DEFAULT_LOCALE_PATH': base_settings.LOCALE_PATHS[0]
}


class Settings(object):

    def __init__(self, user_settings=None, defaults=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or {}

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid API setting: '%s'" % attr)

        val = self.defaults[attr]
        if attr in self.user_settings.keys():
            val = self.user_settings[attr]

        # Cache the result
        setattr(self, attr, val)
        return val


USER_SETTINGS = getattr(base_settings, SETTINGS_KEY, None)
package_settings = Settings(USER_SETTINGS, DEFAULTS)
