#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""


from core.data import result
from core.data import api


class Output(object):
    def __init__(self):
        self.logger = api.logger
        self.result = result
        self.keys = self.get_keys()

    def save(self, output_file):
        pass

    def get_keys(self):
        for key in ['root_domain', 'ip', 'domain']:
            for item in self.result[key].values():
                if item.keys():
                    return item.keys()
