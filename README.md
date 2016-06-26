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

To run the tests
-------

```sh
$ python manage.py test
```


Contributing
-------
1. Fork it
2. Create your feature branch (git checkout -b new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create new Pull Request


Links
-------

* https://github.com/onesky/api-documentation-platform
* https://developer.oneskyapp.com/


Licence
-------------
The MIT License (MIT)

Copyright (c) 2016 Bahattin Çiniç

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
