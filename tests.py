from mock import patch
from unittest import TestCase

from cyanite import CyaniteFinder
from graphite_api.storage import FindQuery


class CyaniteTests(TestCase):
    def test_conf(self):
        config = {'cyanite': {'urls': ['http://host1:8080',
                                       'http://host2:9090']}}
        CyaniteFinder(config)
        from cyanite import urls
        self.assertEqual(urls.host, 'http://host1:8080')
        self.assertEqual(urls.host, 'http://host2:9090')
        self.assertEqual(urls.host, 'http://host1:8080')

    @patch('requests.get')
    def test_metrics(self, get):
        get.return_value.json.return_value = [
            {'path': 'foo.',
             'leaf': 0},
            {'path': 'foo.bar',
             'leaf': 1},
        ]
        finder = CyaniteFinder({'cyanite': {'url': 'http://host:8080'}})
        query = FindQuery('foo.*', 50, 100)
        branch, leaf = list(finder.find_nodes(query))
        self.assertEqual(leaf.path, 'foo.bar')
        self.assertEqual(branch.path, 'foo.')
        get.assert_called_once_with('http://host:8080/paths',
                                    params={'query': 'foo.*'})

        get.reset_mock()
        get.return_value.json.return_value = {
            'from': 50,
            'to': 100,
            'step': 1,
            'series': {'foo.bar': list(range(50))},
        }

        time_info, data = leaf.reader.fetch(50, 100)
        self.assertEqual(time_info, (50, 100, 1))
        self.assertEqual(data, list(range(50)))

        get.assert_called_once_with('http://host:8080/metrics',
                                    params={'to': 100,
                                            'path': 'foo.bar',
                                            'from': 50})

    @patch('requests.get')
    def test_fetch_multi(self, get):
        get.return_value.json.return_value = [
            {'path': 'foo.baz',
             'leaf': 1},
            {'path': 'foo.bar',
             'leaf': 1},
        ]

        finder = CyaniteFinder({'cyanite': {'url': 'http://host:8080'}})
        query = FindQuery('foo.*', 50, 100)
        nodes = list(finder.find_nodes(query))

        get.reset_mock()
        get.return_value.json.return_value = {
            'from': 50,
            'to': 100,
            'step': 1,
            'series': {'foo.bar': list(range(50)),
                       'foo.baz': list(range(50))},
        }

        time_info, series = finder.fetch_multi(nodes, 50, 100)
        self.assertEqual(set(series.keys()), set(['foo.bar', 'foo.baz']))
