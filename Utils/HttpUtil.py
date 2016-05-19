# -*- coding: utf-8 -*-
import requests


class OpenstackRestful(object):
    def __init__(self, tokenId):
        self.tokenId = tokenId

    def update_token(self, token):
        self.tokenId = token

    def get_req(self, url):
        headers = {'Content-type': 'application/json', 'X-Auth-Token': self.tokenId}
        return requests.get(url, headers=headers).json()

    def post_req(self, url, post_data):
        headers = {'Content-type': 'application/json', 'X-Auth-Token': self.tokenId}
        r = requests.post(url, json=post_data, headers=headers)
        print r.status_code
        return r.status_code
