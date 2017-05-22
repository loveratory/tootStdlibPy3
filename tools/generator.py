# -*- cording: utf-8 -*-

import json
import os
import sys
import urllib.parse
import urllib.request

def generator (path):
    mastodon_url = input('mastodon server url > ')
    registry_app_payload = json.dumps({
        'client_name': 'tootStdlibPy3',
        'redirect_uris': 'urn:ietf:wg:oauth:2.0:oob',
        'scopes': 'read write'
    })
    # request headers
    headers = {
        'content-type': 'application/json',
        'user-agent': 'tootStdlibPy3 +https://github.com/BindEmotions/tootStdlibPy3'
    }
    # request app generation to /api/v1/apps
    registry_app_request = urllib.request.Request(
        urllib.parse.urljoin(mastodon_url, '/api/v1/apps'),
        registry_app_payload.encode('utf-8'),
        headers
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
        headers
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
    return config

if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) == 2 else 'config.json'
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../',
        filename
    )
    config = generator(path)
    with open(path, 'w') as f:
        json.dump(config, f, sort_keys=True, indent=4)
