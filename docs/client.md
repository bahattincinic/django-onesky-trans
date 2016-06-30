## Client Examples

- [Project](#detail-of-project)
- [Project Group](#list-of-project-groups)
- [Order](#create---create-a-new-order)


### Detail of Project

```python
from django_onesky.client import ProjectClient

client = ProjectClient()
client.get_project_detail(project_id=1000)
```

### Remove project

```python
from django_onesky.client import ProjectClient

client = ProjectClient()
client.remove_project(project_id=1000)
```

### Update Project

```python
from django_onesky.client import ProjectClient

client = ProjectClient()
client.update_project(project_id=1000, name="New Name")
```

### List languages of a project

```python
from django_onesky.client import ProjectClient

client = ProjectClient()
client.get_project_languages(project_id=1000)
```

### List of uploaded files for given project.

```python
from django_onesky.client import ProjectClient

client = ProjectClient()
client.get_project_file_list(project_id=1000, page=1)
```


### Add or update translations by file

```python
from django_onesky.client import ProjectClient

client = ProjectClient()
client.project_file_upload(project_id=1000, file_name='django.po',
                           file_format='GNO_PO', locale='en',
                           is_keeping_all_strings=True)
```

### Download project translation

```python
from django_onesky.client import ProjectClient

client = ProjectClient()
client.project_file_upload(project_id=1000, source_file_name='django.po',
                           export_file_name='django.po', locale='en')
```


### List of project groups

```python
from django_onesky.client import ProjectGroupClient

client = ProjectGroupClient()
client.get_project_groups_list()
```

### Detail of project groups

```python
from django_onesky.client import ProjectGroupClient

client = ProjectGroupClient()
client.get_project_list(project_group_id=1)
```

### List of projects for project group

```python
from django_onesky.client import ProjectGroupClient

client = ProjectGroupClient()
client.get_project_list(project_group_id=1)
```

## List of Orders

### List of project groups

```python
from django_onesky.client import OrderClient

client = OrderClient()
client.get_order_list(project_id=1)
```


Click the following link for more information:

* https://github.com/onesky/api-documentation-platform