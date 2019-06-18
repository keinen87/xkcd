import os
from dotenv import load_dotenv


load_dotenv()

PATH = os.getenv('PATH_TO_IMAGES', 'images')
API_URL_TEMPLATE = 'https://api.vk.com/method/'
PARAMS_TEMPLATE = {
    'access_token': os.environ['ACCESS_TOKEN'],
    'group_id': os.environ['GROUP_ID'],
    'v': os.environ['API_VERSION']
}
