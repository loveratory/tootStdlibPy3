import urllib.parse
import urllib.request
import json

class Request:
    def __init__ (self, config):
        self.base_url = urllib.parse.urljoin(config.get('mastodon_url', 'meta'), '/api/v1/')
        self.headers = {
            'content-type': 'application/json',
            'user-agent': 'tootStdlibPy3 +https://github.com/BindEmotions/tootStdlibPy3',
            'authorization': '{} {}'.format(config.get('token_type'), config.get('access_token'))
        }

    def post (self, endpoint, data):
        request_url = urllib.parse.urljoin(self.base_url, endpoint)
        request_payload = json.dumps(data)
        request = urllib.request.Request(
            request_url,
            request_payload.encode('utf-8'),
            self.headers
        )
        try:
            with urllib.request.urlopen(request) as res:
                code = res.getcode()
                data = json.loads(res.read())
        except urllib.error.HTTPError as e:
            code = e.getcode()
            data = json.loads(e.read())
        return [code, data]
