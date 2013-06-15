"""
Created on 2011-03-28
RestClient performs REST-protocol communication with the construction tier

@author: Bohdan Mushkevych
"""

import json
from rest_client.restful_lib import Connection

from settings import settings


class ConnectionPool(object):
    def __init__(self, logger, login, pwd, hosts):
        self.logger = logger
        self.index = 0

        self.connection_pool = []
        for host in hosts:
            try:
                connection = Connection(host, username=login, password=pwd)
                connection.h.disable_ssl_certificate_validation = True
                self.connection_pool.append(connection)
            except Exception as e:
                self.logger.error('Exception occurred while connecting to %s:%s ' % (host, str(e)), exc_info=True)
                        
    def get_connection(self):
        pool_len = len(self.connection_pool)
        if pool_len == 0:
            raise EnvironmentError('ConnectionPool is empty. Unable to serve connection')

        if self.index >= pool_len:
            self.index = 0
        
        current = self.connection_pool[self.index]
        self.index += 1
        return current


class RestClient(object):
    REQUEST_CLIENT     = '/admin/clients'

    ARGUMENT_SITES     = 'domains'
    ARGUMENT_TIMESTAMP = 'timestamp'

    def __init__(self, logger):
        login = settings['construction_login']
        pwd = settings['construction_password']
        hosts = settings['construction_hosts']
        self.logger = logger
        self.connection_pool = ConnectionPool(logger, login, pwd, hosts)
    
    def _perform_communication(self, request, body_as_dict):
        conn = self.connection_pool.get_connection()
        resp = conn.request_post(request,
                                 body=json.dumps(body_as_dict),
                                 headers={'content-type': 'application/json', 'accept': 'application/json'})
        status = resp[u'headers']['status']
        # check that we either got a successful response (200) or a previously retrieved, but still valid response (304)
        if status == '200' or status == '304':
            return json.loads(resp[u'body'])
        else:
            self.logger.error('Request failed with status %s' % str(status))
            return dict()

    def _sites_membership(self, request, timestamp, list_of_sites):
        body_as_dict = dict()
        body_as_dict[self.ARGUMENT_TIMESTAMP] = timestamp
        body_as_dict[self.ARGUMENT_SITES] = list_of_sites
        return self._perform_communication(request, body_as_dict)

    def get_client_mapping(self, timestamp, list_of_sites):
        return self._sites_membership(self.REQUEST_CLIENT, timestamp, list_of_sites)


if __name__ == '__main__':
    pass