import os
import requests
from random import randint
from settings import PATH, API_URL_TEMPLATE, PARAMS_TEMPLATE


def fetch_random_comic(path):
    current_comic_url = 'http://xkcd.com/info.0.json'
    response = requests.get(current_comic_url)
    response.raise_for_status()
    comics_count = response.json()['num']
    number = randint(1, comics_count)
    comics_url = 'http://xkcd.com/{}/info.0.json'.format(number)
    response = requests.get(comics_url)
    response.raise_for_status()
    comment = response.json()['alt']
    image_url = response.json()['img']
    filename = os.path.join(path, 'comic{}.png'.format(number))
    response = requests.get(image_url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)
        return filename, comment


def get_upload_url(api_url_template, params):
    api_method = 'photos.getWallUploadServer'
    url = '{}{}'.format(api_url_template, api_method)
    response = requests.get(url, params=params)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']
    return upload_url


def upload_photo(api_url_template, params, upload_url, filepath):
    image_file_descriptor = open(filepath, 'rb')
    files = {
        'file': image_file_descriptor,
        'Content-Type': 'image/jpeg'
    }
    response = requests.post(upload_url, params=params, files=files)
    image_file_descriptor.close()
    response.raise_for_status()
    params['photo'] = response.json()['photo']
    params['server'] = response.json()['server']
    params['hash'] = response.json()['hash']
    return params


def save_wall_photo(api_url_template, params):     
    api_method = 'photos.saveWallPhoto'
    save_url = '{}{}'.format(api_url_template, api_method)
    response = requests.post(save_url, params=params)
    response.raise_for_status()
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
    response.raise_for_status()


if __name__ == '__main__':
    os.makedirs(PATH, exist_ok=True)
    filepath, comment = fetch_random_comic(PATH)
    upload_url = get_upload_url(API_URL_TEMPLATE, PARAMS_TEMPLATE)
    params = upload_photo(API_URL_TEMPLATE, PARAMS_TEMPLATE, upload_url, filepath)
    media_id, owner_id = save_wall_photo(API_URL_TEMPLATE, params)
    post_photo(API_URL_TEMPLATE, PARAMS_TEMPLATE, media_id, owner_id, comment)
    os.remove(filepath)
