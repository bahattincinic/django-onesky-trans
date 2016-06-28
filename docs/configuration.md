Configuration
---

Add to your settings.py

```sh
INSTALLED_APPS = (
    ...
    'django_onesky'
)

ONESKY_CONFIG = {
    'BASE_URL': 'https://platform.api.onesky.io/1/', # optional
    'PUBLIC_KEY': '<public key>',
    'PRIVATE_KEY': '<private key>',
    'PO_TRANSLATE_PROJECT': <project id>,
    'ENABLED': True, # optional
}
```

if you add custom code in this command, you can override makemessages or compile messages command,


```python

class MakeMessagesProcess(object):

    def __call__(self, options):
        pass


class CompileMessagesProcess(object):

    def __call__(self, options):
        pass
```

```python
ONESKY_CONFIG = {
    ...
    'MAKE_MESSAGES_PROCESS_CLASS': 'path.file.MakeMessagesProcess',
    'COMPILE_MESSAGES_PROCESS_CLASS': 'path.file.CompileMessagesProcess'
}
```