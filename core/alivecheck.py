#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import re

from core.data import api
from core.data import result
from comm.progressbar import Bar
from comm.coroutine import WorkerPool


class AliveCheck(object):

    def __init__(self):
        self.exit_flag = False
        self.req = api.request
        self.count_max = 0

    def __check_targets(self):
        self.wp = WorkerPool()
        title_regex = re.compile("<title>(.*?)<\/title>", re.DOTALL | re.M)
        for key in ['root_domain', 'ip', 'domain']:
            for item in result[key]:
                self.count_max += 1
                self.wp.add_job(
                    self.__load_targets,
                    result[key][item],
                    title_regex
                )
        self.bar = Bar('AliveCheck', max=self.count_max)
        self.wp.run()
        self.bar.finish()

    def __load_targets(self, target, title_regex):
        try:
            req = self.req.request(
                'GET', 'http://' + target['domain'], timeout=5)
        except:
            pass
        else:
            target['status_code'] = req.status_code
            if req.status_code == 200:
                content = req.content
                title_match = title_regex.search(content)
                target['title'] = title_match.group(1) if title_match else 'failed'
        finally:
            self.bar.next()

    def __init_targets(self):
        for key in ['root_domain', 'ip', 'domain']:
            for item in result[key]:
                result[key][item]['status_code'] = 'unkonwn'
                result[key][item]['title'] = 'unkonwn'

    def exit(self):
        self.exit_flag = True

    def start(self):
        self.__init_targets()
        self.__check_targets()
