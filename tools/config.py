# -*- cording: utf-8 -*-

import json
import os
import sys
import urllib.parse
import urllib.request

class Config:
    ''' simple configuration loader '''
    def __init__(self, path):
        self.path = path
        self.load()

    def get(self, element, scope = 'access_token'):
        if element not in self.config[scope]:
            return None
        return self.config[scope][element]

    def load(self):
        try:
            with open(self.path, 'r') as f:
                self.config = json.load(f)
        except:
            traceback = sys.exc_info()[2]
            raise Exception('no configuration found, you can generate by tools/generator.py.').with_traceback(traceback)
