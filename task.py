from storage import storage_client

PREPARE = 0
PROCESS = 1
SUCCESS = 2
FAILED = 3


class Task:

    def __init__(self, task_id: str, download_url: str, file_name: str, upload_url: str) -> None:
        self.status = PREPARE
        self._task_id = task_id
        self._download_url = download_url
        self._file_name = file_name
        self._upload_url = upload_url

    @property
    def task_id(self):
        return self._task_id

    @property
    def download_url(self):
        return self._download_url

    @property
    def file_name(self):
        return self._file_name

    @property
    def upload_url(self):
        return self._upload_url

    def run(self):
        self.status = PROCESS
        storage_client.put_object_from_url_with_url(self._upload_url, self._download_url)
        self.status = SUCCESS

    def cancel(self):
        pass
