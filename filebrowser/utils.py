"""
    filebrowser.utils
    
"""
import commands
import logging
import os
from django.conf import settings

_logger = logging.getLogger('bigpandamon-filebrowser')


def get_rucio_account():
    """
        get_rucio_account
        
    """
    return getattr(settings, "RUCIO_ACCOUNT", "atlpan")


def get_x509_proxy():
    """
        get_x509_proxy
        
    """
    return getattr(settings, \
                "X509_USER_PROXY", \
                "/data/atlpan/x509up_u25606")


def get_capath():
    """
        get_capath
        
    """
    return getattr(settings, \
                "CAPATH", \
                "/etc/grid-security/certificates")


def get_rucio_redirect_host():
    """
        get_rucio_redirect_host
        
    """
    return getattr(settings, \
                "RUCIO_REDIRECT_HOST", \
                "https://voatlasrucio-redirect-prod-01.cern.ch")


def get_rucio_rest_api_auth_host():
    """
        get_rucio_rest_api_auth_host
        
    """
    return getattr(settings, \
                "RUCIO_AUTH_HOST", \
                "https://voatlasrucio-auth-prod.cern.ch")


def get_rucio_rest_api_server_host():
    """
        get_rucio_rest_api_server_host
        
    """
    return getattr(settings, \
                "RUCIO_SERVER_HOST", \
                "https://voatlasrucio-server-prod.cern.ch")


def get_my_settings():
    """
        get_my_settings()
        
        Get environment settings for the filebrowser.
        
    """
    my_settings = {}

    ### RUCIO_ACCOUNT="atlpan"
    my_settings['RUCIO_ACCOUNT'] = get_rucio_account()

    ### Rucio redirect host
    my_settings['RUCIO_REDIRECT_HOST'] = get_rucio_redirect_host()

    ### Rucio REST API Auth host
    my_settings['RUCIO_AUTH_HOST'] = get_rucio_rest_api_auth_host()

    ### Rucio REST API server host
    my_settings['RUCIO_SERVER_HOST'] = get_rucio_rest_api_server_host()

    my_settings['X509_USER_PROXY'] = get_x509_proxy()

    ### CAPATH
    my_settings['CAPATH'] = get_capath()

    return my_settings


def get_rucio_oauth_token():
    """
        get_rucio_oauth_token ... get Rucio OAuth Token
        
        return: the Rucio OAuth token
    """
    ### init the Rucio OAuth Token
    rucioToken = ''

    ### assemble the curl command
    cmd = ' curl -s -i -H "X-Rucio-Account: %(rucio_account)s" --cacert %(proxy)s --cert %(proxy)s --capath %(capath)s -X GET %(rucio_api_host)s/auth/x509_proxy ' \
        % {
           'rucio_account': get_rucio_account(), \
           'proxy': get_x509_proxy(), \
           'capath': get_capath(), \
           'rucio_api_host': get_rucio_rest_api_auth_host() \
         }
    cmd += ' | grep "X-Rucio-Auth-Token: " | sed -e "s#X-Rucio-Auth-Token: ##g" '
    _logger.info('get_rucio_oauth_token: cmd=(%s)' % cmd)

    ### get the curl command output
    status, output = commands.getstatusoutput(cmd)

    ### get the rucioToken
    rucioToken = output.rstrip()

    ### return the Rucio OAuth Token
    return rucioToken


def get_rucio_metalink_file(rucioToken, lfn, scope):
    """
        get_rucio_metalink_file ... get Rucio metalink file with replicas of the lfn
        @params
            rucioToken ... Rucio OAuth Token
            lfn ... file name, e.g. log.blahblah.tgz
            scope ... Rucio scope, e.g. "user", or "data13_8tev"
        
        returns: content of Rucio metalink file as json string 
    """
    ### get the metalink file for scope:lfn
    cmd = ' RUCIO_TOKEN="%(rucio_token)s" ;  curl -s --cacert %(proxy)s --capath %(capath)s  -H "X-Rucio-Auth-Token: $RUCIO_TOKEN"  -H "Accept: application/x-json-stream"  -X GET \'%(rucio_api_host)s/replicas/%(scope)s/%(lfn)s\' ' % \
        { \
            'rucio_api_host': get_rucio_rest_api_server_host(), \
            'proxy': get_x509_proxy(), \
            'capath': get_capath(), \
            'rucio_token': rucioToken, \
            'lfn': lfn, \
            'scope': scope, \
        }
    _logger.info('get_rucio_oauth_token: cmd=(%s)' % cmd)

    ### get the metalink file
    status, output = commands.getstatusoutput(cmd)

    ### return the Rucio metalink file
    return output


