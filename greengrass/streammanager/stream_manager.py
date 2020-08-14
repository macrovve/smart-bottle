import asyncio
import json
import logging
import time

from configs import STREAM_MANAGER_OUTPUT_IOT_CHANNEL
from configs import STREAM_NAME
from greengrasssdk.stream_manager import ExportDefinition
from greengrasssdk.stream_manager import IoTAnalyticsConfig
from greengrasssdk.stream_manager import MessageStreamDefinition
from greengrasssdk.stream_manager import Persistence
from greengrasssdk.stream_manager import StrategyOnFull
from greengrasssdk.stream_manager import StreamManagerException
from greengrasssdk.stream_manager.streammanagerclient import StreamManagerClient


class BottleStreamManagerClient(object):
    _logger = logging.getLogger(__name__)

    def __init__(self):
        self.stream_manager_client = StreamManagerClient()

        try:
            self.stream_manager_client.create_message_stream(MessageStreamDefinition(
                name=STREAM_NAME,  # Required.
                max_size=268435456,  # Default is 256 MB.
                stream_segment_size=16777216,  # Default is 16 MB.
                time_to_live_millis=None,  # By default, no TTL is enabled.
                strategy_on_full=StrategyOnFull.OverwriteOldestData,  # Required.
                persistence=Persistence.File,  # Default is File.
                flush_on_write=False,  # Default is false.
                export_definition=ExportDefinition(
                    # Optional. Choose where/how the stream is exported to the AWS Cloud.
                    kinesis=None,
                    iot_analytics=[
                        IoTAnalyticsConfig(identifier="IoTAnalyticsExport" + STREAM_NAME,
                                           iot_channel=STREAM_MANAGER_OUTPUT_IOT_CHANNEL)])))

        except StreamManagerException:
            pass
        # Properly handle errors.
        except ConnectionError or asyncio.TimeoutError:
            pass

        # Properly handle errors.

    def append_state(self, weight, type_):
        payload = {
            "weight": weight,
            "type": type_,
            "timestamp": time.time()
        }

        self.stream_manager_client.append_message(STREAM_NAME, json.dumps(payload).encode("utf-8"))
        self._logger.info("Append the state {} to the stream {}".format(payload, STREAM_NAME))

    def read_state(self):
        pass
