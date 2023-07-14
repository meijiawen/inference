import requests

url = 'http://127.0.0.1:7860/'
files = [('files', open('./beignets-task-guide.png', 'rb'))]

resp = requests.post(url=url, files=files)
print(resp.json())