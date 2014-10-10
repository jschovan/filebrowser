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
'url'        ... url of the log file from where you can download it (located on PanDA mon machine), default value is _None_,
'errors'     ... dictionary with list of errors encountered, 
'status'     ... log file status in PanDA DB, 
'guid'       ... GUID of the file as recorded in PanDA DB, 
'pfns'       ... list of pfns, 
'scope'      ... Rucio scope of the log file,
'lfn'        ... file name of the log file, 
'site'       ... PanDA resource/DDM endpoint where the log file is located (according to PanDA DB),
'timestamp'  ... datetime in isoformat, time when the response has been sent,
  ```
