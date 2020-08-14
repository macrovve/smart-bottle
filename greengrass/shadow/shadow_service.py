import json
import logging

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient


class ShadowService(object):
    _logger = logging.getLogger(__name__)

    def __init__(self, client_id, endpoint, endpoint_port, root_ca_path, private_key_path, certificate_path):
        self.client_id = client_id
        self.endpoint = endpoint
        self.endpoint_port = endpoint_port
        self.root_ca_path = root_ca_path
        self.private_key_path = private_key_path
        self.certificate_path = certificate_path

        self.state = {}

        # AWSIoTMQTTShadowClient configuration
        self.client = AWSIoTMQTTShadowClient(self.client_id)
        self.client.configureEndpoint(self.endpoint, self.endpoint_port)
        self.client.configureCredentials(self.root_ca_path, self.private_key_path, self.certificate_path)
        self.client.configureAutoReconnectBackoffTime(1, 32, 20)
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec

        # Connect to AWS IoT
        self.client.connect()

        self.device_shadow = self.client.createShadowHandlerWithName(client_id, True)
        self.device_shadow.shadowGet(self._shadow_get_callback, 5)

        self.device_shadow.shadowRegisterDeltaCallback(self._shadow_delta_callback)

    def _shadow_get_callback(self, payload, response_status, token):
        if response_status == "timeout":
            self._logger.info("Shadow get request" + token + " time out!")
        if response_status == "accepted":
            payload_dict = json.loads(payload)
            self._logger.info("Get request with token: " + token + " accepted")
            self._logger.info("state of shadow: ", payload_dict["state"]["desired"])
        if response_status == "rejected":
            self._logger.info("Shadow get request" + token + " rejected!")

    def _shadow_delta_callback(self, payload, response_status, token):
        if response_status == "timeout":
            self._logger.info("Shadow Delta request" + token + " time out!")

        # TODO not sure about the status code, didn't find the document
        # if response_status == "accepted":
        payload_dict = json.loads(payload)
        delta = payload_dict['state']

        self._logger.info("Request to update the reported state...")
        self._shadow_acknowledge_state(delta)

        self.state.update(delta)
        self._logger.info("State of shadow is {}".format( delta))

    def _shadow_update_callback(self, payload, response_status, token):
        if response_status == "timeout":
            self._logger.info("Shadow update request" + token + " time out!")
        if response_status == "accepted":
            payload_dict = json.loads(payload)

            self._logger.info("Update request with token: " + token + " accepted")
            self._logger.info("state of shadow: {}".format(payload_dict["state"]["desired"]))
        if response_status == "rejected":
            self._logger.info("Shadow update request" + token + " rejected!")

    def _shadow_acknowledge_state(self, acknowledge_state):
        payload = {
            "state": {
                "reported": acknowledge_state
            }
        }

        self.device_shadow.shadowUpdate(json.dumps(payload), None, 5)

    def update_state(self, state):
        payload = {
            "state": {
                "desired": state
            }
        }

        self.device_shadow.shadowUpdate(json.dumps(payload), self._shadow_update_callback, 5)

    def get_state(self):
        return self.state
