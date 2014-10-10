__author__ = 'pike'
import urllib2
import json

class OpenstackRestful:

    def __init__(self, tokenId):
        self.tokenId = tokenId

    def getResult(self, url, postData = None):
        serverRequest = urllib2.Request(url)
        serverRequest.add_header("Content-type", "application/json")
        serverRequest.add_header("X-Auth-Token", self.tokenId)

        response = urllib2.urlopen(serverRequest)
        result = json.loads(response.read())
        return result