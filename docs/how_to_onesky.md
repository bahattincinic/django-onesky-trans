How to OneSky?
---
- Create project
- Choose website/webapp, private/public
- Choose default language (professional translation service only works with english as default)
- Upload empty django.po file, or also upload all your translated django.po files and select proper language for them.
- Choose language pairs (according to uploaded translations and your django app settings)
- Translate or order translation using OneSky
- Mark translations as "ready to publish"

---

- Configure your django app for django-oneskyapp tool
- Use manage.py oneskyapp management command to pull, make, push, compile translations
- Restart your django app

---

- Add new strings to your django app
- Use manage.py oneskyapp
- Translate using OneSky
- Use manage.py oneskyapp
- Restart your django app


We copied from https://github.com/pista329/django-oneskyapp.