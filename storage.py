import logging
import requests

import oss2
from tqdm import tqdm


class StorageClient:

    def __init__(self, ak: str, sk: str, endpoint: str, bucket: str):
        self.ak = ak
        self.sk = sk
        self.endpoint = endpoint
        self.bucket = bucket
        self.client = oss2.Bucket(oss2.Auth(ak, sk), endpoint, bucket)

    def put_object(self, object_name: str, local_path: str):
        self.client.put_object_from_file(object_name, local_path)

    def append_object(self, object_name: str, position: int, data):
        return self.client.append_object(object_name, position, data)

    def put_object_from_url(self, object_name: str, download_url: str):
        rsp = requests.get(download_url, stream=True)
        self.client.put_object(object_name, rsp)

    def check_exist(self, object_name: str):
        return self.client.object_exists(object_name)

    def put_object_with_url(self, data, sign_url: str):
        self.client.put_object_with_url(sign_url, data)

    def pre_sign(self, object_name: str):
        return self.client.sign_url('PUT', object_name, 60)


class StorageClientWrapper:

    def __init__(self):

        self.oss_client = StorageClient("LTAI5tQMnQveWBRcof7Kwums", "0JbV3sYwcJ3TIwmWQ7MCE5ppWpcVE8", 
                                    "https://oss-cn-shanghai.aliyuncs.com", "openmmlab-open")

    @staticmethod
    def download_progress(url: str, local_path: str):
        rsp = requests.get(url, stream=True)
        total = int(rsp.headers.get('content-length', 0))
        with open(local_path, 'wb+') as file, tqdm(total=total, unit='iB', unit_scale=True, unit_divisor=1024) as bar:
            for data in rsp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)


    @staticmethod
    def fetch_object_from_url(url: str, local_path: str):
        StorageClientWrapper.download_progress(url, local_path)
        return local_path

    def put_object(self, object_name: str, local_path: str):
        self.oss_client.put_object(object_name, local_path)

    def put_object_from_url(self, object_name: str, download_url: str):
        rsp = requests.get(download_url, stream=True)
        total = int(rsp.headers.get('content-length', 0))
        position = 0
        with tqdm(total=total, unit='iB', unit_scale=True, unit_divisor=1024) as bar:
            for data in rsp.iter_content(chunk_size=1024):
                result = self.oss_client.append_object(object_name, position, data)
                bar.update(result.next_position - position)
                position = result.next_position

    def put_object_from_url_with_url(self, sign_url: str, download_url: str):
        logging.info(f"begin download file {download_url}")
        rsp = requests.get(download_url, stream=True)
        self.oss_client.put_object_with_url(rsp, sign_url)
    
    def check_exist(self, object_name: str):
        return self.oss_client.check_exist(object_name)

    def pre_sign(self, object_name: str):
        return self.oss_client.pre_sign(object_name)
    


storage_client = StorageClientWrapper()


# sign_url = storage_client.pre_sign("models/dev/weight/demooooooo/test-create-page12321haha/test-create-page1/tt")
# storage_client.put_object_from_url_with_url(sign_url, "https://www.baidu.com")