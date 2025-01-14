import socket
import requests
import os

class Esp:
    connect=socket.socket

class update():
    def __init__(self):
        self.resourceDir=self.getUrl('https://github.com/Karnilov/SmartHome')

    def getUrl(self, link):

        lk = link.split('/')
        for q in range(3):
            del lk[0]
        owner = lk[0]
        del lk[0]
        repo = lk[0]
        del lk[0]
        path = '/'.join(lk)
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        return url

    def download_file(self, file_url, folder_path):
        response = requests.get(file_url)
        filename = os.path.join(folder_path, file_url.split('/')[-1])
        with open(filename, 'wb') as f:
            f.write(response.content)
            print(f'Скачан файл: {filename}')

    def download_folder_contents(self, folder_url, folder_path):
        response = requests.get(folder_url)
        if response.status_code == 200:
            contents = response.json()
            os.makedirs(folder_path, exist_ok=True)
            for item in contents:
                if item['type'] == 'file':
                    self.download_file(item['download_url'], folder_path)
                elif item['type'] == 'dir':
                    new_folder_path = os.path.join(folder_path, item['name'])
                    self.download_folder_contents(item['url'], new_folder_path)

    def update(self):
        self.download_folder_contents(self.resourceDir, 'download/')