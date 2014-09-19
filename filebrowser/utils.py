"""
    filebrowser.utils
    
"""
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


def getRucioOAuthToken():
    """
        getRucioOAuthToken ... get Rucio OAuth Token
        @params
            rucioAccount  ...  $RUCIO_ACCOUNT
            x509Proxy     ...  $X509_USER_PROXY
        
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
    _logger.info('getRucioOAuthToken: cmd=(%s)' % cmd)

    ### get the curl command output
    status, output = commands.getstatusoutput(cmd)

    ### get the rucioToken
    rucioToken = output.rstrip()

    ### return the Rucio OAuth Token
    return rucioToken


