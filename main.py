import requests
import os
from urllib.parse import urlsplit
from dotenv import load_dotenv

load_dotenv(dotenv_path='config.env')
header = {'Authorization': f'Bearer {os.getenv("TOKEN")}'}
api_url = 'https://api-ssl.bitly.com/v4'

def user_request():
    user = '/user'
    response = requests.get(f'{api_url}{user}', headers=header)
    response.raise_for_status()
    return response.json()

def shorten_link(link):
    bitlinks = '/bitlinks'
    params_for_request = {'long_url': link}
    respons = requests.post(f'{api_url}{bitlinks}', headers = header, json=params_for_request)
    respons.raise_for_status()
    return respons.json()['link']


def count_clicks(link):
    bitlink_parts = urlsplit(link)
    summary = f'/bitlinks/{bitlink_parts.netloc}{bitlink_parts.path}/clicks/summary'
    request_params = {'unit': 'day',
                      'units':'-1'}
    respons = requests.get(f'{api_url}{summary}', headers = header, params=request_params)
    respons.raise_for_status()
    return respons.json()['total_clicks']



if __name__ == "__main__":
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
