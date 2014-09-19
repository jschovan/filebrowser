FileBrowser
=====

FileBrowser is a simple Django app to browse file information in ATLAS BigPanDA 
monitor. Providing the file scope and LFN, user can view the files.

Quick start
-----------

1. Add "filebrowser" to your INSTALLED_APPS setting like this::
```
INSTALLED_APPS = (
    ...
    'filebrowser',
    ....
)
``` 
If you are using django.js in your site app, do not forget to update JS_I18N_APPS_EXCLUDE.

2. Add templates of "filebrowser" to TEMPLATE_DIRS setting like this::
```
import filebrowser
TEMPLATE_DIRS = (
    ...
    join(dirname(filebrowser.__file__), 'templates'),
    ...
)
```

3. Include the filebrowser URLconf in your project urls.py like this::
```
url(r'^filebrowser/', include('filebrowser.urls')),
```

4. Visit http://127.0.0.1:8000/filebrowser/ to browse the files.

