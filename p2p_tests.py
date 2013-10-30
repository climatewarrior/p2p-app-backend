#!/usr/bin/python

import unittest
import p2p
import requests
import base64
import json
import code
import random

unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: random.choice([1,-1])    

class P2PTests(unittest.TestCase):
        
    def setUp(self):
        p2p.app.config['TESTING'] = True
        self.app = p2p.app.test_client()
        self.url = "http://localhost:5000"
        
    def tearDown(self):
        pass

    def test_register(self):
        data = {'username':'testUser', 'password':'testPass', \
                'email':'test@test.com'}

        headers = {'content-type': 'application/json'}
        rv = requests.post(self.url + '/register', data=json.dumps(data),\
                           headers=headers)

        self.assertEqual(rv.status_code, 201)

    def test_add_question(self):
        headers = {'content-type': 'application/json'}
        data= { 'title': 'Test Question', 'content': 'This is a sample question', 'tags':''}
        rv = requests.post(self.url + '/questions', data = json.dumps(data), \
                           auth=('testUser', 'testPass'), \
                           headers=headers)

        assert 'question' in rv.json()
        
if __name__ == '__main__':
    unittest.main()
