FileBrowser
=====

FileBrowser is a simple Django app to browse file information in ATLAS BigPanDA 
monitor. Providing the file scope and LFN, GUID and site name, user can view the files.

Quick start
-----------

1. Add "filebrowser" to your INSTALLED_APPS setting like this:
  ```
INSTALLED_APPS = (
    ...
    'filebrowser',
    ....
)
  ``` 
  If you are using django.js in your site app, do not forget to update JS_I18N_APPS_EXCLUDE.

2. Add templates of "filebrowser" to TEMPLATE_DIRS setting like this:
  ```
import filebrowser
TEMPLATE_DIRS = (
    ...
    join(dirname(filebrowser.__file__), 'templates'),
    ...
)
  ```
  List filebrowser templates only after your Django site's templates, to allow for template extension.  

3. Add "filebrowser" directory name to settings:
  ```
FILEBROWSER_DIRECTORY = "filebrowser"
  ```
  This directory will be under MEDIA_ROOT.

4. Configure proxy settings:
  ```
X509_USER_PROXY = "/data/atlpan/x509up_u25606"
CAPATH = "/etc/grid-security/certificates"
  ```

5. Configure Rucio client settings:
  ```
RUCIO_ACCOUNT = "atlpan"
RUCIO_REDIRECT_HOST = "https://rucio-lb-prod.cern.ch"
RUCIO_AUTH_HOST = "https://voatlasrucio-auth-prod.cern.ch"
RUCIO_SERVER_HOST = "https://voatlasrucio-server-prod.cern.ch"
  ```

6. Include the filebrowser URLconf in your project urls.py like this:
  ```
url(r'^filebrowser/', include('filebrowser.urls')),
  ```

7. Visit http://127.0.0.1:8000/filebrowser/ to browse the files.

8. Run unit tests from your Django site area:
  ```
python manage.py test filebrowser.tests
  ```
