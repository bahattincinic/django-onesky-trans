# django-onesky-trans
OneSky integration for your Django app

## How to install

You can install django-onesky-trans using **pip**

    pip install django-onesky-trans

or via sources:

    python setup.py install

## Features
django-onesky-trans support all the features provided via oneskyapp.com APIs, such as:

* Manage projects
* Import translation files
* Export translation files


Configuration
---

Add to your settings.py

```sh
INSTALLED_APPS = (
    ...
    'django_onesky_trans'
)

ONESKY_CONFIG = {
    'BASE_URL': 'https://platform.api.onesky.io/1/',
    'PUBLIC_KEY': '<public key>',
    'PRIVATE_KEY': '<private key>',
    'PO_TRANSLATE_PROJECT': <prorject id>,
    'ENABLED': True,
}
```

Management command Usage
---

```sh
$ python manage.py onesky_makemessages --help
  Usage: ./manage.py onesky_makemessages [options]
  
  Updates .po translation files using makemessages and uploads them to OneSky translation service.
  Pushes new translation stringsfrom OneSky to django app and compiles messages.
  
  Options:
    -v VERBOSITY, --verbosity=VERBOSITY
                          Verbosity level; 0=minimal output, 1=normal output,
                          2=verbose output, 3=very verbose output
    --settings=SETTINGS   The Python path to a settings module, e.g.
                          "myproject.settings.main". If this isn't provided, the
                          DJANGO_SETTINGS_MODULE environment variable will be
                          used.
    --pythonpath=PYTHONPATH
                          A directory to add to the Python path, e.g.
                          "/home/djangoprojects/myproject".
    --traceback           Raise on exception
    --no-color            Don't colorize the command output.
    --version             show program's version number and exit
    -h, --help            show this help message and exit
```
