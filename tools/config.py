# -*- cording: utf-8 -*-

import json
import os
import urllib.parse
import urllib.request

class Config:
    ''' simple configuration loader '''
    def __init__(self, path):
        self.path = path

    def get(self, element, scope = 'access_token'):
        if element not in self.config[scope]:
            return None
        return self.config[scope][element]

    def load(self):
        try:
            self.config = self.loader()
        except:
            self.config = self.generator()

    def loader(self):
        with open(self.path, 'r') as f:
            j = json.load(f)
        return j

    def generator(self):
        mastodon_url = input('mastodon server url > ')
        registry_app_payload = json.dumps({
            'client_name': 'tootStdlibPy3',
            'redirect_uris': 'urn:ietf:wg:oauth:2.0:oob',
            'scopes': 'read write'
        })
        # request app generation to /api/v1/apps
        registry_app_request = urllib.request.Request(
            urllib.parse.urljoin(mastodon_url, '/api/v1/apps'),
            registry_app_payload.encode('utf-8'),
            { 'content-type': 'application/json' }
        )
        with urllib.request.urlopen(registry_app_request) as res:
            app = json.loads(res.read())
        # show url for requesting access code to user
        access_code_payload = urllib.parse.urlencode({
            'client_id': app['client_id'],
            'response_type': 'code',
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'
        })
        print('please access {} and input an access code to below.'.format(
            urllib.parse.urljoin(mastodon_url, '/oauth/authorize?' + access_code_payload)))
        access_code = input('access code > ')
        # get access token
        access_token_payload = json.dumps({
            'grant_type': 'authorization_code',
            'client_id': app['client_id'],
            'client_secret': app['client_secret'],
            'code': access_code,
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
            'scope': 'write'
        })
        access_token_request = urllib.request.Request(
            urllib.parse.urljoin(mastodon_url, '/oauth/token'),
            access_token_payload.encode('utf-8'),
            { 'content-type': 'application/json' }
        )
        with urllib.request.urlopen(access_token_request) as res:
            access_token = json.loads(res.read())
        # save its
        config = {
            'access_token': access_token,
            'app': app,
            'meta': {
                'mastodon_url': urllib.parse.urljoin(mastodon_url, '/')
            }
        }
        with open(self.path, 'w') as f:
            json.dump(config, f)
        return config
