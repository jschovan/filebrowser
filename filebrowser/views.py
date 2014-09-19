"""
    filebrowser.views
    
"""
import logging
#from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
#from django.core.urlresolvers import reverse
#from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

_logger = logging.getLogger('bigpandamon-filebrowser')


def index(request):
    """
        index -- filebrowser's default page
        
        :param request: Django's HTTP request 
        :type request: django.http.HttpRequest
        
    """
    ### set request response data
    data = {}
    return render_to_response('filebrowser/index.html', data, RequestContext(request))


