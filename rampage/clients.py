# Copyright (c) 2015 Platform9 systems. All rights reserved

# pylint: disable=too-few-public-methods

import logging
import os

from keystoneclient import session as ksc_session
from keystoneclient.auth.identity import v3
from keystoneclient.v3 import client as keystone_v3
from novaclient import client as nc
from glanceclient.v2 import client as glance_v2
from cinderclient.v2 import client as cinder_v2

from neutronclient.neutron import client as neutronclient

LOG = logging.getLogger(__name__)

class Clients(object):
    """
    Class to encapsulate info and operations on regions. Gives access
    to endpoints and urls, and authentication information.
    FIXME: Eventually add nova, glance, cinder etc clients as members
    """

    def __init__(self):
        auth_url = os.environ['OS_AUTH_URL'].replace('v2.0', 'v3')
        user = os.environ['OS_USERNAME']
        passwd = os.environ['OS_PASSWORD']
        project_name = os.environ['OS_TENANT_NAME']

        auth = v3.Password(auth_url=auth_url, username=user, password=passwd,
                           project_name=project_name, user_domain_name='default',
                           project_domain_name='default')

        session = ksc_session.Session(auth=auth, verify=False)
        self.keystone = keystone_v3.Client(session=session)

        self.nova = nc.Client(2, session=session)
        self.glance = glance_v2.Client(session=session)
        self.cinder = cinder_v2.Client(session=session)
        self.neutron = neutronclient.Client('2.0', session=session)

    def get_endpoint(self, service_name):
        region_name = os.environ['OS_REGION_NAME']
        service = self.keystone.services.list(name=service_name)[0]
        eps = self.keystone.endpoints.list(interface='public',
                                           service=service,
                                           region_name=region_name)
        assert(len(eps) == 1)
        return eps[0].url
