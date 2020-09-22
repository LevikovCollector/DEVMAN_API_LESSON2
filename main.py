import requests
import os
from urllib.parse import urlsplit
from dotenv import load_dotenv

def shorten_link(link):
    bitlinks = '/bitlinks'
    params_for_request = {'long_url': link}
    respons = requests.post(f'{API_URL}{bitlinks}', headers = HEADER, json=params_for_request)
    respons.raise_for_status()
    return respons.json()['link']


def count_clicks(link):
    bitlink_parts = urlsplit(link)
    summary = f'/bitlinks/{bitlink_parts.netloc}{bitlink_parts.path}/clicks/summary'
    request_params = {'unit': 'day',
                      'units':'-1'}
    respons = requests.get(f'{API_URL}{summary}', headers = HEADER, params=request_params)
    respons.raise_for_status()
    return respons.json()['total_clicks']



if __name__ == "__main__":
    load_dotenv(dotenv_path='config.env')
    HEADER = {'Authorization': f'Bearer {os.getenv("BITLY_TOKEN")}'}
    API_URL = 'https://api-ssl.bitly.com/v4'

    user_link = input('Введите ссылку: ')
    short_link = None
    if user_link.startswith('https://bit.ly'):
        try:
            count_click = count_clicks(user_link)
            print(f'Количество кликов по ссылке: {count_click}')
        except requests.exceptions.HTTPError as error:
            print(f'При получении количества кликов по ссылке "{short_link}" \nВозникла ошибка: {error}')
    else:
        try:
            short_link = shorten_link(user_link)
            print('Битлинк:', short_link)
        except requests.exceptions.HTTPError as error:
            print(f'При обработке ссылки возникла ошибка: {error} \nПроверьте введенную ссылку: {user_link}')
