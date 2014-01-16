__author__ = 'pike'

CeilometerHost="114.212.189.132"

from OpenstackService import  *

class Ceilometer(OpenstackService):

    def __init__(self):
        OpenstackService.__init__(self)


    def getAllMeters(self):
        url="http://%s:8777/v1/meters" % CeilometerHost
        print url
        serverRequest=urllib2.Request(url)
        serverRequest.add_header("Content-type","application/json")
        serverRequest.add_header("X-Auth-Token",self.tokenid)
        request=urllib2.urlopen(serverRequest)
        result=json.loads(request.read())
        print result

    def getCpuStat(self):pass


if __name__=="__main__":

    ceilometertest=Ceilometer()
    ceilometertest.getAllMeters()
