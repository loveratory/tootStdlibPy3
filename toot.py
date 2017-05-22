import os
import sys

from tools.config import Config
from tools.request import Request

if __name__ == '__main__':
    status = sys.stdin.read()
    filename = sys.argv[1] if len(sys.argv) == 2 else 'config.json'
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        filename
    )
    config = Config(path)
    request = Request(config)
    result = request.post('statuses', {
        'status': status
    })
    if 'error' in result[1]:
        print('an error "{}" occurred while posting a toot.'.format(result[1]['error']), file=sys.stderr)
        exit(1)
    else:
        print(result[1]['url'])
