# -*- coding: utf-8 -*-
import urllib
import urllib2
import unittest
import json

import constants

host = 'http://localhost:5000'

class EnqueueServerTestCase(unittest.TestCase):
    def setUp(self):
        """Before each test, set up a blank database"""
        pass

    def tearDown(self):
        """Get rid of the database again after each test."""
        pass

    def createRequest(self, uri, http_method):
        class MethodCustomRequest(urllib2.Request):
            def get_method(self):
                return http_method
        return MethodCustomRequest(uri)

    def buildUri(self, path, query=None):
        uri = None
        if( query ):
            uri = '%s%s?%s' % ( host, path, query )
        else:
            uri = '%s%s' % ( host, path )
        return uri

    def post(self, path, data=''):
        req = urllib2.Request(self.buildUri(path))
        jsondata = json.dumps(data)
        req.add_header('Content-type', 'application/json')
        try:
            response = urllib2.urlopen(req,jsondata)
        except urllib2.HTTPError, e:
            if e.code != 201:
                return None
        return response

    def delete(self, path, data=''):
        req = self.createRequest(self.buildUri(path), 'DELETE')
        jsondata = json.dumps(data)
        req.add_header('Content-type', 'application/json')
        try:
            response = urllib2.urlopen(req, jsondata)
        except urllib2.HTTPError, e:
            return None
        return response

    def get(self, path, query=None):
        query_string = None
        if query!=None:
            query_string = urllib.urlencode(query)
        req = urllib2.Request(self.buildUri(path, query_string))
        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            return None
        return response

    def test_01_chk(self):
        response = self.get('/')
        data = json.loads(response.read())
        self.assertEqual(response.code, 200, 'Check OK')
        self.assertEqual(data['status'], 'ok', 'return status is okay')

    def test_02_enqueue(self):
        data = {
            'pns': [
                {
                    'app'  : 'test',
                    'type' : 'i',
                    'token': 'testtesttest',
                    'badge': 0,
                    'text' : 'test message 1'
                },
                {
                    'app'  : 'test',
                    'type' : 'i',
                    'token': 'testtesttest',
                    'badge': 0,
                    'text' : 'test message 2'
                }
             ]
        }
        response = self.post('/enqueue', data)
        data = json.loads(response.read())
        self.assertEqual(response.code, 201, 'Created')
        self.assertEqual(data['enqueue'], 2, '2 message enqueued')

if __name__ == '__main__':
    unittest.main()
