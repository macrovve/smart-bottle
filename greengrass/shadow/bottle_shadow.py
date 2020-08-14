import time

from configs import CLIENT_ID
from configs import GGC_CA_PATH
from configs import IOT_ENDPOINT
from configs import IOT_ENDPOINT_PORT
from configs import PATH_TO_THING_CERTIFICATE
from configs import PATH_TO_THING_PRIVATE_KEY
from configs import PATH_TO_ROOT_CA
from greengrass.shadow.shadow_service import ShadowService

import logging


class BottleShadow(object):
    _logger = logging.getLogger(__name__)
    def __init__(self):
        # In the doc, sometime the Endpoint could be 127.0.0.1 recorded in the ggc-host file
        # print("{} {} {} {} {} {}".format(CLIENT_ID, IOT_ENDPOINT, str(IOT_ENDPOINT_PORT), GGC_CA_PATH, THING_PRIVATE_KEY_PATH, THING_CERTIFICATE_PATH))
        # self._logger.info("{} {} {} {} {} {}".format(CLIENT_ID, IOT_ENDPOINT, str(IOT_ENDPOINT_PORT), GGC_CA_PATH, THING_PRIVATE_KEY_PATH, THING_CERTIFICATE_PATH))
        self.bottle_shadow = ShadowService(
            client_id=CLIENT_ID,
            endpoint=IOT_ENDPOINT,
            endpoint_port=IOT_ENDPOINT_PORT,
            root_ca_path=PATH_TO_ROOT_CA,
            private_key_path=PATH_TO_THING_PRIVATE_KEY,
            certificate_path=PATH_TO_THING_CERTIFICATE)

    def get_water_in_the_bottle(self):
        return self.bottle_shadow.get_state().get("water_in_the_bottle")

    def get_water_type_in_the_bottle(self):
        return self.bottle_shadow.get_state().get("water_type_in_the_bottle")

    def schedule(self):
        pass

    def set_water_type_in_the_bottle(self):
        pass

    def set_water_in_the_bottle(self, weight):
        self.bottle_shadow.update_state({"water_in_the_bottle" : weight})






if __name__ == '__main__':
    bottle_shadow = BottleShadow()
    while True :
        bottle_shadow.set_water_in_the_bottle(10)
        time.sleep(1)
        print(bottle_shadow.get_water_in_the_bottle())





