"""
    filebrowser.views
    
"""
import logging
#from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
#from django.core.urlresolvers import reverse
#from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .utils import get_rucio_pfns_from_guids, fetch_file, get_filebrowser_vo


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
#            print 'error:', msg
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
#        _logger.info('guid=' + guid)
    except:
        pass
    try:
        site = request.GET['site']
#        _logger.info('site=' + site)
    except:
        pass
    try:
        lfn = request.GET['lfn']
#        _logger.info('lfn=' + lfn)
    except:
        pass
    try:
        scope = request.GET['scope']
#        _logger.info('scope='+scope)
    except:
        pass

    if 'missingparameter' not in errors.keys():
        pfns, errtxt = get_rucio_pfns_from_guids(guids=[guid], site=[site], \
                    lfns=[lfn], scopes=[scope])
#        if not len(pfns):
#            msg = 'File lookup failed. [guid=%s, site=%s, scope=%s, lfn=%s]' % \
#                (guid, site, scope, lfn)
#            _logger.warning(msg)
#            errors['lookup'] = msg
        if len(errtxt):
            if 'lookup' not in errors:
                errors['lookup'] = ''
            errors['lookup'] += errtxt

    ### download the file
    files = []
    dirprefix = ''
    if len(pfns):
        pfn = pfns[0]
        files, errtxt, dirprefix = fetch_file(pfn, guid)
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
        'scope': scope, \
        'lfn': lfn, \
        'site': site, \
        'guid': guid, \
        'viewParams' : {'MON_VO': str(get_filebrowser_vo()).upper()}, \
    }
    return render_to_response('filebrowser/index.html', data, RequestContext(request))


