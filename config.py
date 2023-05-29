import os
import uuid

TRANSFER_AGENT_LABEL = "TRANSFER_AGENT_LABEL"
TRANSFER_SERVER_ENDPOINT = "TRANSFER_SERVER_ADDRESS"
TRANSFER_AGENT_PING_TIMEOUT = "TRANSFER_AGENT_PING_TIMEOUT"
TRANSFER_AGENT_ID = "TRANSFER_AGENT_ID"

LOGGER_LEVEL = "LOGGER_LEVEL"

class Config:

    def __init__(self) -> None:
        self._label = os.getenv(TRANSFER_AGENT_LABEL, "normal")
        self._server_endpoint = os.getenv(TRANSFER_SERVER_ENDPOINT, "https://dev.openxlab.org.cn/gw/model-center")
        self._ping_timeout = os.getenv(TRANSFER_AGENT_PING_TIMEOUT, 5)

        self._agent_id = os.getenv(TRANSFER_AGENT_PING_TIMEOUT, str(uuid.uuid1()))
        self._logger_level = os.getenv(LOGGER_LEVEL, "INFO")

    @property
    def label(self):
        return self._label

    @property
    def server_endpoint(self):
        return self._server_endpoint

    @property
    def agent_id(self):
        return self._agent_id

    @property
    def ping_timeout(self):
        return self._ping_timeout

    @property
    def logger_level(self):
        return self._logger_level


config = Config()