import requests
import json

from requests.models import Response

from config import config
from task import Task, SUCCESS
from logger import logger


class TransferServer:

    def __init__(self) -> None:
        self.config = config
        self.server_endpoint = config.server_endpoint
        self.ping_uri = "/api/v1/transfer/ping"
        self.get_task_uri = "/api/v1/transfer/getTask"
        self.sync_task_uri = "/api/v1/transfer/syncTask"

    def extractSuccess(self, body):
        msgCode = body["msgCode"]
        if msgCode != "10000":
            return None

        data = body["data"]

        return data

    def handle_result(self, response: Response):
        if response.status_code // 100 != 2:
            logger.error("response status: %s, url: %s, text: %s", response.status_code, response.url, response.text)
            return None

        return self.extractSuccess(response.json())

    def post(self, url, data):
        headers = {"Content-Type": "application/json"}
        response = requests.post(url=url, headers=headers, data=json.dumps(data), 
                                 timeout=self.config._ping_timeout)
        return self.handle_result(response)

    def ping(self):
        result = self.post(self.server_endpoint + "/" + self.ping_uri, {
            "label": self.config.label,
            "agentId": self.config.agent_id
        })

        if result is None:
            return False

        return True

    def checkTaskStatus(self):
        pass

    def getTask(self) -> Task:
        result = self.post(self.server_endpoint + "/" + self.get_task_uri, {
            "label": self.config.label,
            "agentId": self.config.agent_id
        })

        if result is None:
            return None

        return Task(result["taskId"], result["downloadUrl"], result["fileName"], result["uploadUrl"])

    def syncTask(self, task: Task):
        result = self.post(self.server_endpoint + "/" + self.sync_task_uri, {
            "label": self.config.label,
            "agentId": self.config.agent_id,
            "taskId": task.task_id,
            "status": task.status
        })

        if result is None:
            return False

        return True


transfer_server = TransferServer()

