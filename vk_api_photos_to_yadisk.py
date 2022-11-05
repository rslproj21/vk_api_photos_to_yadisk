import requests
import yadisk
from tqdm import tqdm
import json

yandex_disk_token = yadisk.YaDisk(token="")
vk_token = ""

vk_url = "https://api.vk.com/method/photos.getAll"
vk_user_id = input("Введите ID пользователя Вконткате: ")
vk_photo_quantity = input("Введите количество фото для сохранения: ")

params = {"owner_id": vk_user_id, "extended": 1, "acces_token": vk_token, "count": vk_photo_quantity, "v": 5.131}

response = requests.get(vk_url, params=params).json()
response = response["response"]["items"]

size_photo_vk = {}
last_photos = {}
full_size = []
json_files = []

for alpha in response:
    likes = alpha["likes"]
    size = alpha["sizes"]

    for beta in size:
        url = beta["url"]
        all_size = url.rpartition("size=")[-1].rpartition("&quality=")[0].split("x")
        summ = int(all_size[0]) + int(all_size[1])
        size_photo_vk[summ] = [beta["url"]]
        full_size.append(alpha)

    some_sorted_func = sorted(size_photo_vk.keys())[-1]
    download_url = size_photo_vk[some_sorted_func]

    while len(full_size) > 1:
        for alpha in full_size:
            if len(full_size) > 1:
                full_size.pop(0)

    for i in full_size:
        for i in alpha["sizes"]:
            if download_url[0] == i["url"]:
                json_file = {"file_name": likes["count"], "size": i["type"]}
                json_files.append(json_file)

    last_photos[download_url[0]] = str(likes["count"])
    full_size.clear()

folder_path = input("Введите название папки для загрузки фото: ")

if not yandex_disk_token.is_dir(folder_path):
    yandex_disk_token.mkdir(folder_path)

for k, v in tqdm(last_photos.items()):
    yandex_disk_token.upload(k, f'{folder_path} / {v}.jpeg')

with open("data_file.json", "w") as write_files:
    json.dump(json_files, write_files)
