import os
import requests
from random import randint
from settings import PATH, API_URL_TEMPLATE, PARAMS_TEMPLATE


def fetch_random_comic(path):
    current_comic_url = 'http://xkcd.com/info.0.json'
    response = requests.get(current_comic_url)
    if response.ok:
        comics_count = response.json()['num']
    number = randint(1, comics_count)
    comics_url = 'http://xkcd.com/{}/info.0.json'.format(number)
    response = requests.get(comics_url)
    if response.ok:
        comment = response.json()['alt']
        image_url = response.json()['img']
        filename = os.path.join(path, 'comic{}.png'.format(number))
        response = requests.get(image_url)
        if response.ok:
            with open(filename, 'wb') as file:
                file.write(response.content)
        return filename, comment


def upload_photo(api_url_template, filepath, params):
    api_method = 'photos.getWallUploadServer'
    upload_url = '{}{}'.format(api_url_template, api_method)
    response = requests.get(upload_url, params=params)
    if response.ok:
        upload_url = response.json()['response']['upload_url']
    image_file_descriptor = open(filepath, 'rb')
    files = {
        'file': image_file_descriptor,
        'Content-Type': 'image/jpeg'
    }
    response = requests.post(upload_url, params=params, files=files)
    image_file_descriptor.close()
    if response.ok:
        photo_parameter = response.json()['photo']
        server_parameter = response.json()['server']
        hash_parameter = response.json()['hash']
    api_method = 'photos.saveWallPhoto'
    save_url = '{}{}'.format(api_url_template, api_method)
    params['photo'] = photo_parameter
    params['server'] = server_parameter
    params['hash'] = hash_parameter
    response = requests.post(save_url, params=params)
    if response.ok:
        media_id = response.json()['response'][0]['id']
        owner_id = response.json()['response'][0]['owner_id']
        return media_id, owner_id


def post_photo(api_url_template, params, media_id, owner_id, comment):
    api_method = 'wall.post'
    api_url = '{}{}'.format(api_url_template, api_method)
    params['owner_id'] = '-{}'.format(params['group_id'])
    params['attachments'] = 'photo{}_{}'.format(owner_id, media_id)
    params['message'] = comment
    response = requests.post(api_url, params=params)
    if response.ok:
        return True


def delete_local_file(path):
    os.remove(path)


if __name__ == '__main__':
    os.makedirs(PATH, exist_ok=True)
    filepath, comment = fetch_random_comic(PATH)
    media_id, owner_id = upload_photo(API_URL_TEMPLATE, filepath, PARAMS_TEMPLATE)
    post_photo(API_URL_TEMPLATE, PARAMS_TEMPLATE, media_id, owner_id, comment)
    delete_local_file(filepath)
