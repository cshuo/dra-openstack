# -*- coding: utf-8 -*-
CONTROLLER_HOST = "20.0.1.10"
COMPUTE1_HOST = "20.0.1.11"
COMPUTE2_HOST = "20.0.1.12"
CEILOMETER_HOST = CONTROLLER_HOST

AUTH_URL = "http://%s:35357" % CONTROLLER_HOST
NOVA_URL = "http://%s:8774" % CONTROLLER_HOST
CEILOMETER_URL = "http://%s:8777" % CEILOMETER_HOST
REST_URL = "http://114.212.189.132:9000/api/"

ZABBIX_URL = "http://20.0.1.12/zabbix/api_jsonrpc.php"
ZABBIX_USER = "Admin"
ZABBIX_PASSWD = "zabbix"
CONTROLLER = 'kolla0'
ZABBIX_WEB_INTERVAL = 30
ZABBIX_TRIGGER_NUM = 2


HOST_USERNAME = "cshuo"
HOST_PASSWORD = "cshuo"

HOST_ROOT_USERNAME = "root"
HOST_ROOT_PASSWORD = "cshuo"

COMPUTE1_HOST_USERNAME = "root"
COMPUTE1_HOST_PASSWORD = "cshuo"

COMPUTE2_HOST_USERNAME = "root"
COMPUTE2_HOST_PASSWORD = "cshuo"


USERNAME = "admin"
TENANTNAME = "admin"
PASSWORD = "artemis"

RABBIT_HTTP_PORT = 15672
RABBIT_HTTP_USER = "guest"
RABBIT_HTTP_PASSWORD = "guest"

DEFAULT_RPC_SERVER = 'pike'

# environment variables
PARAMS = "--os-username %s " % USERNAME + \
         "--os-tenant-name %s " % TENANTNAME + \
         "--os-auth-url %s/v3 " % AUTH_URL + \
         "--os-password %s" % PASSWORD


# Hades compute threshold conf
UNDERLOAD_THRESHOLD = 0
OVERLOAD_THRESHOLD = 80
AVG_TIME_LEN = 0.05  # hour
