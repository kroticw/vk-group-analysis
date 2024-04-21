import csv
import datetime
from numpy import NaN
import requests
import yaml
from yaml import load
import pandas as pd

with open('config.yaml', 'r') as f:
    config = load(f, Loader=yaml.FullLoader)


class cfg():
    token = config['token']
    id = config['app_id']
    vk_url = config['vk_url']
    vk_version = config['vk_version']
    user_id = config['user_id']


def get_posts(group_id):
    params = {'access_token': cfg.token, 'domain': group_id, 'v': 5.131}
    r = requests.get('https://api.vk.com/method/wall.get', params=params)
    count = r.json()['response']['count']
    print(f'Количество публикаций в сообществе: {count}')
    if count > 100:
        return count // 100
    else:
        count = 1
        return count


def get_walls(group_id, posts_df_header):
    with open(f'{group_id}_walls.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(posts_df_header)
        
        for offset in range(0, get_posts(group_id) + 1):
            print("offset: ", offset)
            params = {'access_token': cfg.token, 'domain': group_id, 'v': 5.131, 'offset': offset * 100}
            posts = requests.get('https://api.vk.com/method/wall.get', params=params).json()['response']

            for post in posts['items']:
                record = [post['id'], post.get('text'),
                          datetime.datetime.fromtimestamp(int(post.get('date'))).date(),
                          post.get('views', {}).get('count') if post.get('views') else None,
                          post.get('reposts').get('count') if post.get('reposts') else None,
                          post.get('likes').get('count') if post.get('likes') else None
                          ]
                writer.writerow(record)
                