"""
    filebrowser.views
    
"""
import logging
#from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
#from django.core.urlresolvers import reverse
#from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .utils import get_rucio_pfns_from_guids, fetch_file


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
            if 'missing-parameter' not in errors.keys():
                errors['missing-parameter'] = ''
            errors['missing-parameter'] += msg

    ### if all expected GET parameters are present, execute file lookup
    pfns = []
    guid = ''
    if 'missing-parameter' not in errors.keys():
        guid = request.GET['guid']
        site = request.GET['site']
        lfn = request.GET['lfn']
        scope = request.GET['scope']
        _logger.info('guid='+guid)
        _logger.info('site='+site)
        _logger.info('lfn='+lfn)
        _logger.info('scope='+scope)
        pfns, errtxt = get_rucio_pfns_from_guids(guids=[guid], site=[site], \
                    lfns=[lfn], scopes=[scope])
        if not len(pfns):
            msg = 'File lookup failed. [guid=%s, site=%s, scope=%s, lfn=%s]' % \
                (guid, site, scope, lfn)
            _logger.warning(msg)
            errors['lookup'] = msg
        if len(errtxt):
            if 'lookup' in errors:
                errors['lookup'] += errtxt

    ### download the file
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
    }
    return render_to_response('filebrowser/index.html', data, RequestContext(request))


