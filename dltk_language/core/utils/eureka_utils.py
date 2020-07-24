from properties import REGISTRY

if REGISTRY:
    from py_eureka_client import eureka_client
    import requests
    from properties import *

    HOST = INSTANCE_IP
    PROTOCOL = HTTP
    APPLICATION_NAME = MY_APPLICATION_NAME
    PORT = REG_PORT
    DISCOVERY_SERVICE = DISCOVERY_SERVICE

    INSTANCE_ID = HOST+":"+APPLICATION_NAME+":"+PORT
    HEALTHCHECK_URL = PROTOCOL + HOST + ":" + PORT + "/healthcheck"
    STATUS_URL = PROTOCOL + HOST + ":" + PORT + "/status"
    HOMEPAGE_URL = PROTOCOL + HOST + ":" + PORT
    CONTEXT_PATH = "/" + APPLICATION_NAME


    def get_service_url(SERVICE_NAME):
        url=DISCOVERY_SERVICE+SERVICE_NAME
        try:
            services = requests.get(url,headers={"content-type":"application/json","Accept":"application/json"}).json()
            if services:
                instances = services["application"]["instance"]
                host = instances[0]["hostName"]
                port = instances[0]["port"]["$"]
                return PROTOCOL + host + ":" + str(port)
        except:
            raise Exception("No instance found for this service")


    def register_client():
        eureka_client.init(eureka_server=HTTP + DISCOVERY_SERVICE_IP + COLON + DISCOVERY_SERVICE_PORT + "/eureka/",
                           app_name=APPLICATION_NAME,instance_ip=INSTANCE_IP,
                           instance_port=int(PORT))
