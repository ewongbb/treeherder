# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.

import unittest

from mock import patch
from treeherder.client import PerfherderClient, TreeherderClientError


class PerfherderClientTest(unittest.TestCase):

    def _get_mock_response(self, response_struct):
        class MockResponse(object):

            def json(self):
                return response_struct

            def raise_for_status(self):
                pass

        return MockResponse()

    @patch("treeherder.client.client.requests.get")
    def test_get_performance_signatures(self, mock_get):

        mock_get.return_value = self._get_mock_response(
            {'signature1': {'cheezburgers': 1},
             'signature2': {'hamburgers': 2},
             'signature3': {'cheezburgers': 2}})
        pc = PerfherderClient()
        sigs = pc.get_performance_signatures('mozilla-central')
        self.assertEqual(len(sigs), 3)
        self.assertEqual(sigs.get_signature_hashes(), ['signature1',
                                                       'signature2',
                                                       'signature3'])
        self.assertEqual(sigs.get_property_names(),
                         set(['cheezburgers', 'hamburgers']))
        self.assertEqual(sigs.get_property_values('cheezburgers'), set([1, 2]))

    @patch("treeherder.client.client.requests.get")
    def test_get_performance_signature_properties(self, mock_get):
        mock_get.return_value = self._get_mock_response(
            [{'cheezburgers': 1, 'hamburgers': 2}])
        pc = PerfherderClient()
        propdict = pc.get_performance_signature_properties('mozilla-central',
                                                           'signature1')
        self.assertEqual({'cheezburgers': 1, 'hamburgers': 2},
                         propdict)

    @patch("treeherder.client.client.requests.get")
    def test_get_performance_signature_properties_no_results(self, mock_get):
        mock_get.return_value = self._get_mock_response(
            [])
        pc = PerfherderClient()
        self.assertRaises(TreeherderClientError,
                          pc.get_performance_signature_properties,
                          'mozilla-central', 'signature1')

    @patch("treeherder.client.client.requests.get")
    def test_get_performance_series_list(self, mock_get):

        mock_get.return_value = self._get_mock_response(
            [{'series_signature': 'signature1',
              'blob': [{'geomean': 1}, {'geomean': 2}]},
             {'series_signature': 'signature2',
              'blob': [{'geomean': 2}, {'geomean': 1}]}])
        pc = PerfherderClient()
        series_list = pc.get_performance_series_list('mozilla-central',
                                                     ['signature1',
                                                      'signature2'])
        self.assertEqual(len(series_list), 2)
        self.assertEqual(series_list[0]['geomean'], [1, 2])
        self.assertEqual(series_list[1]['geomean'], [2, 1])

    @patch("treeherder.client.client.requests.get")
    def test_get_performance_series_list_improper_length(self, mock_get):

        # returning 1 when we should return 2
        mock_get.return_value = self._get_mock_response(
            [{'series_signature': 'signature1',
              'blob': [{'geomean': 1}]}])

        pc = PerfherderClient()
        self.assertRaises(TreeherderClientError,
                          pc.get_performance_series_list,
                          'mozilla-central', ['signature1', 'signature2'])
