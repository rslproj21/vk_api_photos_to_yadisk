import os

import requests
import tqdm
import datetime
import time
import argparse
from settings import user_id

class Vkapi:
    def __init__(self, token, rev=False, count=10):
        self.token = token
        self.rev = rev
        self.count = count

    def get_photos(self, id): 
        profile_photos = []
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': self.token,
            'owner_id': id, 
            'album_id': 'profile', 
            'extended': True,
            'count': self.count, 
            'rev': self.rev, 
            'photo_sizes': True, 
            'v': "5.131"}
        
        response = requests.get(url, params=params)
        for photos_size in response.json()["response"]["items"]:
            profile_photos.append({
                "likes": photos_size["likes"]['count'],
                "type": photos_size["sizes"][-1]["type"],
                "url": photos_size["sizes"][-1]["url"],
                "date": photos_size["date"]        
                }
        )
        return profile_photos

    def get_id_by_short_name(self, user_name):
        url = "https://api.vk.com/method/utils.resolveScreenName"
        params = {
            "access_token": self.token,
            "v": "5.131",
            "screen_name": user_name
        }
        response = requests.get(url, params=params)
        if user_name.isdigit():
            return user_name
        else:
            return response.json()['response']['object_id']



class Yandexapi:
    def __init__(self, token, upload_photos):
        self.token = token
        self.upload_photos = upload_photos

    def headers_get(self):
        return {
            "Authorization": f"OAuth {self.token}",
            "Content-Type": "application/json"}

    def createfolder(self, folder_name):
        params = {"path": "disk:/{}/".format(folder_name)}
        headers = self.get_headers()
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        response = requests.put(url, headers=headers, params=params)
        response.status_code
        return folder_name
    
    def yandex_disk_upload(self, folder):
        my_disk = []
        headers = self.headers_get()
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        for urls in tqdm(self.upload_photos):
            if urls["likes"] not in my_disk:
                my_disk.append(urls["likes"])
                path = "disk:/{}/{}.jpg".format(folder, urls["likes"])
            else:
                my_disk.append(urls["likes"])
                value = datetime.datetime.fromtimestamp(urls["date"])
                path = "disk:/{}/{}{}.jpg".format(
                    folder, urls["likes"], f"{value:-%Y-%m-%d}"
                )
                params = {"path": path, "url": urls["url"]}
                time.sleep(1)
                response = requests.post(url, headers=headers, params=params)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Программа сохраняет последние загруженные фото профиля(аватары) на яндекс диск')
    parser.add_argument('user_id', help='Ввидите user_name или ID пользователя')
    parser.add_argument('-c', '--count', help='Ввидите количество фото которые хотите сохранить(defoult = 5)')
    args = parser.parse_args()


    vk = Vkapi(token=os.getenv('VK_token'), count=args.count)
    yandex = Yandexapi( token=os.getenv('Ya_token'), upload_photos=vk.get_photos(id=vk.get_id_by_short_name(args.user_id)))
    folder_name = yandex.createfolder(folder = 'vkontakte')
    yandex.yandex_disk_upload((folder_name))




