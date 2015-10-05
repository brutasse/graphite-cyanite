import itertools
import time

try:
    from graphite_api.intervals import Interval, IntervalSet
    from graphite_api.node import LeafNode, BranchNode
except ImportError:
    from graphite.intervals import Interval, IntervalSet
    from graphite.node import LeafNode, BranchNode

import requests


def chunk(nodelist, length):
    chunklist = []
    linelength = 0
    for node in nodelist:
        # the magic number 6 is because the nodes list gets padded
        # with '&path=' in the resulting request
        nodelength = len(str(node)) + 6

        if linelength + nodelength > length:
            yield chunklist
            chunklist = [node]
            linelength = nodelength
        else:
            chunklist.append(node)
            linelength += nodelength
    yield chunklist


class CyaniteLeafNode(LeafNode):
    __fetch_multi__ = 'cyanite'


class URLs(object):
    def __init__(self, hosts):
        self.iterator = itertools.cycle(hosts)

    @property
    def host(self):
        return next(self.iterator)

    @property
    def paths(self):
        return '{0}/paths'.format(self.host)

    @property
    def metrics(self):
        return '{0}/metrics'.format(self.host)
urls = None
urllength = 8000


class CyaniteReader(object):
    __slots__ = ('path',)

    def __init__(self, path):
        self.path = path

    def fetch(self, start_time, end_time):
        data = requests.get(urls.metrics, params={'path': self.path,
                                                  'from': start_time,
                                                  'to': end_time}).json()
        if 'error' in data:
            return (start_time, end_time, end_time - start_time), []
        if len(data['series']) == 0:
            return
        time_info = data['from'], data['to'], data['step']
        return time_info, data['series'].get(self.path, [])

    def get_intervals(self):
        # TODO use cyanite info
        return IntervalSet([Interval(0, int(time.time()))])


class CyaniteFinder(object):
    __fetch_multi__ = 'cyanite'

    def __init__(self, config=None):
        global urls
        global urllength
        if config is not None:
            if 'urls' in config['cyanite']:
                urls = config['cyanite']['urls']
            else:
                urls = [config['cyanite']['url'].strip('/')]
            if 'urllength' in config['cyanite']:
                urllength = config['cyanite']['urllength']
        else:
            from django.conf import settings
            urls = getattr(settings, 'CYANITE_URLS')
            if not urls:
                urls = [settings.CYANITE_URL]
            urllength = getattr(settings, 'CYANITE_URL_LENGTH', urllength)
        urls = URLs(urls)

    def find_nodes(self, query):
        paths = requests.get(urls.paths,
                             params={'query': query.pattern}).json()
        for path in paths:
            if path['leaf']:
                yield CyaniteLeafNode(path['path'],
                                      CyaniteReader(path['path']))
            else:
                yield BranchNode(path['path'])

    def fetch_multi(self, nodes, start_time, end_time):

        paths = [node.path for node in nodes]
        data = {}
        for pathlist in chunk(paths, urllength):
            tmpdata = requests.get(urls.metrics,
                                   params={'path': pathlist,
                                           'from': start_time,
                                           'to': end_time}).json()
            if 'error' in tmpdata:
                return (start_time, end_time, end_time - start_time), {}

            if 'series' in data:
                data['series'].update(tmpdata['series'])
            else:
                data = tmpdata

        time_info = data['from'], data['to'], data['step']
        return time_info, data['series']
