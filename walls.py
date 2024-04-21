import csv
import datetime
from numpy import NaN
import requests
import pandas as pd


def get_posts(group_id, conf):
    params = {'access_token': conf.token, 'domain': group_id, 'v': conf.vk_version}
    r = requests.get(f'{conf.vk_url}/method/wall.get', params=params)
    count = r.json()['response']['count']
    print(f'Количество публикаций в сообществе: {count}')
    if count > 100:
        return count // 100
    else:
        count = 1
        return count


def get_walls(group_id, posts_df_header, conf):
    with open(f'csv/{group_id}_walls.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(posts_df_header)
        
        for offset in range(0, get_posts(group_id, conf) + 1):
            print("offset: ", offset)
            params = {'access_token': conf.token, 'domain': group_id, 'v': conf.vk_version, 'offset': offset * 100}
            posts = requests.get(f'{conf.vk_url}/method/wall.get', params=params).json()['response']

            for post in posts['items']:
                record = [post['id'], post.get('text'),
                          datetime.datetime.fromtimestamp(int(post.get('date'))).date(),
                          post.get('views', {}).get('count') if post.get('views') else None,
                          post.get('reposts').get('count') if post.get('reposts') else None,
                          post.get('likes').get('count') if post.get('likes') else None
                          ]
                writer.writerow(record)
                