FileBrowser API
=====

FileBrowser is a simple Django app to browse file information in ATLAS BigPanDA 
monitor. Providing the file scope and LFN, GUID and site name, user can view the files. 

For more information please see https://github.com/PanDAWMS/panda-bigmon-atlas-filebrowser .

API: ?pandaid=XYZ
-----------
The 'pandaid' parameter is compulsory.

The API has 3 HTTP return states: 200, 404, 400.

**200 OK**: _pandaid_ was provided, log file found in DB, no errors while downloading.

**404 NOT FOUND**: _pandaid_ was provided (but does not exist), or no file found for that pandaid. Example of returned error message:
  ```
'errors': {'lookup': 'Log file for this job has not been found. '}
  ```
**400 BAD REQUEST**:

* When _pandaid_ has not been provided, following error message is produced:
  ```
'errors': {'missingparameter': 'Missing expected GET parameter pandaid. '}
  ```
* For another error the error dictionary contains keys _lookup_ or _download_.


In any case, the data dictionary with the following keys is returned in the response: 
  ```
'pandaid'    ... PanDA job ID,
'url'        ... url of the log file from where you can download it (located on PanDA mon machine), 
                 default value is _None_,
'errors'     ... dictionary with list of errors encountered, 
'status'     ... log file status in PanDA DB, 
'guid'       ... GUID of the file as recorded in PanDA DB, 
'pfns'       ... list of pfns, 
'scope'      ... Rucio scope of the log file,
'lfn'        ... file name of the log file, 
'site'       ... PanDA resource/DDM endpoint where the log file is located (according to PanDA DB),
'timestamp'  ... datetime in isoformat, time when the response has been sent,
  ```


**Example usage**:

Successful pass:
  ```
# curl -v -H 'Accept: application/json' -H 'Content-Type: application/json' "http://HOSTNAME/filebrowser/api/?pandaid=2283871569"
* About to connect() to HOSTNAME port 80 (#0)
*   Trying IP-ADDRESS... connected
> GET /filebrowser/api/?pandaid=2283871569 HTTP/1.1
> User-Agent: curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3
> Host: HOSTNAME
> Accept: application/json
> Content-Type: application/json
> 
< HTTP/1.1 200 OK
< Date: Fri, 10 Oct 2014 22:08:06 GMT
< Server: Apache
< Vary: Cookie
< X-Frame-Options: SAMEORIGIN
< Connection: close
< Transfer-Encoding: chunked
< Content-Type: text/html; charset=utf-8
< 
{'pandaid': 2283871569, 'status': '', 'guid': u'385b39fc-2d9b-4ea2-a1e4-6868a5c7b227', 'errors': {}, 'pfns': [u'srm://srm.HOSTNAME:8443/srm/managerv2?SFN=/atlas/atlasscratchdisk/rucio/panda/d5/71/panda.1010085117.729582.lib._4221268.255649786.log.tgz'], 'timestamp': '2014-10-10T22:08:14.011839', 'url': u'http://HOSTNAME/media/filebrowser/385b39fc-2d9b-4ea2-a1e4-6868a5c7b227/panda.1010085117.729582.lib._4221268.255649786.log.tgz', 'scope': u'panda', 'lfn': u'panda.1010085117.729582.lib._4221268.255649786.log.tgz', 'site': u'ANALY_SITE'}
* Closing connection #0
  
  ```

Missing _pandaid_ parameter:
  ```
# curl -v -H 'Accept: application/json' -H 'Content-Type: application/json' "http://HOSTNAME/filebrowser/api/?pandaid="
* About to connect() to HOSTNAME port 80 (#0)
*   Trying IP-ADDRESS... connected
> GET /filebrowser/api/?pandaid= HTTP/1.1
> User-Agent: curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3
> Host: HOSTNAME
> Accept: application/json
> Content-Type: application/json
> 
< HTTP/1.1 400 BAD REQUEST
< Date: Fri, 10 Oct 2014 22:07:36 GMT
< Server: Apache
< Vary: Cookie
< X-Frame-Options: SAMEORIGIN
< Connection: close
< Transfer-Encoding: chunked
< Content-Type: text/html; charset=utf-8
< 
{'pandaid': None, 'status': '', 'guid': '', 'errors': {'missingparameter': 'Missing expected GET parameter pandaid. '}, 'pfns': [], 'timestamp': '2014-10-10T22:07:37.106266', 'url': None, 'scope': '', 'lfn': '', 'site': ''}
* Closing connection #0

  ```


Non-existing _pandaid_:
  ```
# curl -v -H 'Accept: application/json' -H 'Content-Type: application/json' "http://HOSTNAME/filebrowser/api/?pandaid=228387156900"
* About to connect() to HOSTNAME port 80 (#0)
*   Trying IP-ADDRESS... connected
> GET /filebrowser/api/?pandaid=228387156900 HTTP/1.1
> User-Agent: curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3
> Host: HOSTNAME
> Accept: application/json
> Content-Type: application/json
> 
< HTTP/1.1 404 NOT FOUND
< Date: Fri, 10 Oct 2014 22:15:26 GMT
< Server: Apache
< Vary: Cookie
< X-Frame-Options: SAMEORIGIN
< Connection: close
< Transfer-Encoding: chunked
< Content-Type: text/html; charset=utf-8
< 
{'pandaid': 228387156900, 'status': '', 'guid': '', 'errors': {'lookup': 'Log file for this job has not been found. '}, 'pfns': [], 'timestamp': '2014-10-10T22:15:26.548599', 'url': None, 'scope': '', 'lfn': '', 'site': ''}
* Closing connection #0

  ```


