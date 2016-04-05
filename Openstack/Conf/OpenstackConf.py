# -*- coding: utf-8 -*-
CONTROLLER_HOST = "20.0.1.11"
COMPUTE1_HOST = "20.0.1.21"
COMPUTE2_HOST = "20.0.1.31"
#NETWORKING_HOST = ""
CEILOMETER_HOST = CONTROLLER_HOST

AUTH_URL = "http://%s:35357" % CONTROLLER_HOST
NOVA_URL = "http://%s:8774" % CONTROLLER_HOST
CEILOMETER_URL = "http://%s:8777" % CEILOMETER_HOST

HOST_USERNAME = "vagrant"
HOST_PASSWORD = "cshuo"

HOST_ROOT_USERNAME = "root"
HOST_ROOT_PASSWORD = "cshuo"

COMPUTE1_HOST_USERNAME = "root"
COMPUTE1_HOST_PASSWORD = "cshuo"

COMPUTE2_HOST_USERNAME = "root"
COMPUTE2_HOST_PASSWORD = "cshuo"


USERNAME = "admin"
TENANTNAME = "admin"
PASSWORD = "cshuo"

# environment variables
PARAMS = "--os-username %s " % USERNAME + \
         "--os-tenant-name %s " % TENANTNAME + \
         "--os-auth-url %s/v3 " % AUTH_URL + \
         "--os-password %s" % PASSWORD

