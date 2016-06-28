## Client Examples

### Detail of Project

```python
from django_onesky.client import OneSkyClient

client = OneSkyClient()
client.get_project_detail(project_id=1000)
```

### List languages of a project

```python
from django_onesky.client import OneSkyClient

client = OneSkyClient()
client.get_project_languages(project_id=1000)
```

### List of uploaded files for given project.

```python
from django_onesky.client import OneSkyClient

client = OneSkyClient()
client.get_project_file_list(project_id=1000, page=1)
```


### Add or update translations by file

```python
from django_onesky.client import OneSkyClient

client = OneSkyClient()
client.project_file_upload(project_id=1000, file_name='django.po',
                           file_format='GNO_PO', locale='en',
                           is_keeping_all_strings=True)
```

### Download project translation

```python
from django_onesky.client import OneSkyClient

client = OneSkyClient()
client.project_file_upload(project_id=1000, source_file_name='django.po',
                           export_file_name='django.po', locale='en')
```

Click the following link for more information:

* https://github.com/onesky/api-documentation-platform