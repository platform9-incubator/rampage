# Copyright (c) Platform9 systems. All rights reserved

import json
import logging
import os
import requests

LOG = logging.getLogger(__name__)

def get_token():
    """
    The python keystoneclient doesn't provide a way to get a v3 nocatalog
    token, so this function gets one from the api.
    """
    auth_url = os.environ['OS_AUTH_URL'].replace('v2.0', 'v3')
    url = "%s/auth/tokens?nocatalog" % auth_url

    body = {
        "auth":{
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": os.environ['OS_USERNAME'],
                        "domain": {"id": "default"},
                        "password": os.environ['OS_PASSWORD']
                    }
                }
            },
            "scope": {
                "project": {
                    "name": os.environ['OS_TENANT_NAME'],
                    "domain": { "id": "default" }
                }
            }
        }
    }
    resp = requests.post(url,
                         data=json.dumps(body),
                         headers={'content-type': 'application/json'},
                         verify=False)
    resp.raise_for_status()
    return resp.headers['X-Subject-Token']

