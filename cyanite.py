import time

try:
    from graphite_api.intervals import Interval, IntervalSet
    from graphite_api.node import LeafNode, BranchNode
except ImportError:
    from graphite.intervals import Interval, IntervalSet
    from graphite.node import LeafNode, BranchNode

import requests

PATH_URL = None
METRIC_URL = None


class CyaniteReader(object):
    __slots__ = ('path',)

    def __init__(self, path):
        self.path = path

    def fetch(self, start_time, end_time):
        data = requests.get(METRIC_URL, params={'path': self.path,
                                                'from': start_time,
                                                'to': end_time}).json()
        if 'error' in data:
            return (start_time, end_time, end_time - start_time), []
        time_info = data['from'], data['to'], data['step']
        return time_info, data['series'][self.path]

    def get_intervals(self):
        # TODO use cyanite info
        start = time.time() - 3600 * 2
        end = max(start, time.time())
        return IntervalSet([Interval(start, end)])


class CyaniteFinder(object):
    def __init__(self, config=None):
        global PATH_URL
        global METRIC_URL
        if config is not None:
            url = config['cyanite']['url'].strip('/')
        else:
            from django.conf import settings
            url = settings.CYANITE_URL
        PATH_URL = '{0}/paths'.format(url)
        METRIC_URL = '{0}/metrics'.format(url)

    def find_nodes(self, query):
        paths = requests.get(PATH_URL, params={'query': query.pattern}).json()
        for path in paths:
            if path['leaf']:
                yield LeafNode(path['path'], CyaniteReader(path['path']))
            else:
                yield BranchNode(path['path'])
