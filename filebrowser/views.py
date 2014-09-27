"""
    filebrowser.views
    
"""
import logging
#from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
#from django.core.urlresolvers import reverse
#from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .utils import get_rucio_pfns_from_guids, fetch_file, get_filebrowser_vo, \
get_filebrowser_hostname


_logger = logging.getLogger('bigpandamon-filebrowser')


def index(request):
    """
        index -- filebrowser's default page
        
        :param request: Django's HTTP request 
        :type request: django.http.HttpRequest
        
    """
    errors = {}

    ### check that all expected parameters are in URL
    expectedFields = ['guid', 'site', 'scope', 'lfn']
    for expectedField in expectedFields:
        try:
            request.GET[expectedField]
        except:
            msg = 'Missing expected GET parameter %s. ' % expectedField
            _logger.error(msg)
            if 'missingparameter' not in errors.keys():
                errors['missingparameter'] = ''
            errors['missingparameter'] += msg

    ### if all expected GET parameters are present, execute file lookup
    pfns = []
    scope = ''
    lfn = ''
    guid = ''
    site = ''
    try:
        guid = request.GET['guid']
    except:
        pass
    try:
        site = request.GET['site']
    except:
        pass
    try:
        lfn = request.GET['lfn']
    except:
        pass
    try:
        scope = request.GET['scope']
    except:
        pass

    if 'missingparameter' not in errors.keys():
        pfns, errtxt = get_rucio_pfns_from_guids(guids=[guid], site=[site], \
                    lfns=[lfn], scopes=[scope])
        if len(errtxt):
            if 'lookup' not in errors:
                errors['lookup'] = ''
            errors['lookup'] += errtxt

    ### download the file
    files = []
    dirprefix = ''
    tardir = ''
    if len(pfns):
        pfn = pfns[0]
        files, errtxt, dirprefix, tardir = fetch_file(pfn, guid)
        if not len(pfns):
            msg = 'File download failed. [pfn=%s guid=%s, site=%s, scope=%s, lfn=%s]' % \
                (pfn, guid, site, scope, lfn)
            _logger.warning(msg)
            errors['download'] = msg
        if len(errtxt):
            if 'download' in errors:
                errors['download'] += errtxt

    ### return the file page


    ### set request response data
    data = { \
        'errors': errors, \
        'pfns': pfns, \
        'files': files, \
        'dirprefix': dirprefix, \
        'tardir': tardir, \
        'scope': scope, \
        'lfn': lfn, \
        'site': site, \
        'guid': guid, \
        'viewParams' : {'MON_VO': str(get_filebrowser_vo()).upper()}, \
        'HOSTNAME': get_filebrowser_hostname() \
#        , 'new_contents': new_contents
    }
    return render_to_response('filebrowser/index.html', data, RequestContext(request))


