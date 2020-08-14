# shadow_client
# mqtt_client
# stream_manager_client
import logging
import os

from configs import IOT_ENDPOINT
from configs import PATH_TO_ROOT_CA
from configs import CLIENT_ID
from configs import PATH_TO_THING_PRIVATE_KEY
from configs import PATH_TO_THING_CERTIFICATE
from configs import THING_NAME
from configs import GGC_HOST_PATH
from configs import GGC_CA_PATH

from greengrass.discovery import discoverGGC
from greengrass.discovery import getGGCAddr
logger = logging.getLogger(__name__)

host = IOT_ENDPOINT
iot_CA_path = PATH_TO_ROOT_CA
certificate_path = PATH_TO_THING_CERTIFICATE
private_key_path = PATH_TO_THING_PRIVATE_KEY
thing_name = THING_NAME
client_id = CLIENT_ID

# Run Discovery service to check which GGC to connect to, if it hasn't been run already
# Discovery talks with the IoT cloud to get the GGC CA cert and ip address

if not os.path.isfile("./groupCA/root-ca.crt"):
    discoverGGC(host, iot_CA_path, certificate_path, private_key_path, client_id)
else:
    logger.info("Greengrass core has already been discovered.")
    print("Greengrass core has already been discovered.")

# read GGC Host Address from file
ggcAddr = getGGCAddr(GGC_HOST_PATH)

print("GGC Host Address: " + ggcAddr)
print("GGC Group CA Path: " + GGC_CA_PATH)
print("Private Key of lightController thing Path: " + private_key_path)
print("Certificate of lightController thing Path: " + certificate_path)
print("Client ID(thing name for lightController): " + client_id)
print("Target shadow thing ID(thing name for trafficLight): " + thing_name)

from greengrass.shadow.bottle_shadow import BottleShadow
from greengrass.streammanager.stream_manager import BottleStreamManagerClient