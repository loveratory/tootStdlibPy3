# -*- cording: utf-8 -*-

import urllib.parse
import urllib.request
import json

class Request:
    def __init__ (self, config):
        self.base_url = urllib.parse.urljoin(config.get('mastodon_url', 'meta'), '/api/v1/')
        self.token = config.get('access_token')
        self.headers = {
            'content-type': 'application/json',
            'user-agent': 'tootStdlibPy3 +https://github.com/BindEmotions/tootStdlibPy3'
        }

    def post (self, endpoint, data):
        request_url = urllib.parse.urljoin(self.base_url, endpoint)
        request_payload = json.dumps(data)
        request = urllib.request.Request(
            request_url,
            request_payload.encode('utf-8'),
            self.headers
        )
        with urllib.request.urlopen(request) as res:
            data = json.loads(res.read())
        return data
