# Author: Lucas Roelser <roesler.lucas@gmail.com>
"""
ssl_expriy_lambda uses the ssl_expiry script to allow you to check a list of
SSL certificate expiration dates via AWS Gateway.

See the README for configuration information
"""


import json
import logging
import os

import ssl_expiry

loglevel = os.environ.get('LOGLEVEL', 'INFO')
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level)

logger = logging.getLogger('SSLVerifyLambda')


def main(event, *args, **kwargs) -> list:
    # use the env var HOSTLIST to define a default list of hostnames
    HOST_LIST = os.environ.get('HOSTLIST', '').split(',')
    EXPIRY_BUFFER = int(os.environ.get('EXPIRY_BUFFER', '14'))

    try:
        # pull any additional hostnames from the potential AWS Gateway
        # event object
        query_params = event.get('params', {}).get('querystring', {})
        additional_hosts = query_params.get('host_list', '').split(',')
    except Exception:
        additional_hosts = []

    # cleanup the host list
    HOST_LIST += additional_hosts
    HOST_LIST = filter(None, (x.strip() for x in HOST_LIST))

    logger.debug('Testing hosts {}'.format(HOST_LIST))
    response = [
        ssl_expiry.test_host(host, buffer_days=EXPIRY_BUFFER)
        for host in HOST_LIST
    ]
    for msg in response:
        if 'error' in msg or 'expire' in msg:
            error = {
                'message': 'Cert Errors',
                'results': response,
                'additional_hosts': additional_hosts,
            }
            raise Exception(json.dumps(error))

    return {
        'message': 'All certs are fine',
        'results': response,
        'additional_hosts': additional_hosts,
    }
