import csv

import requests
import yaml
import pandas as pd

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


class cfg:
    token = config['token']
    id = config['app_id']
    vk_url = config['vk_url']
    vk_version = config['vk_version']
    user_id = config['user_id']


def get_members(group_id):
    params = {'access_token': cfg.token, 'group_id': group_id, 'v': 5.131}
    count = requests.get('https://api.vk.com/method/groups.getMembers', params=params).json()['response']['count']
    return count // 1000 if count > 1000 else 1


def get_users(group_id, users_df_header):
    with open(f'{group_id}_users.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(users_df_header)

        for offset in range(0, get_members(group_id) + 1):
            print("offset: ", offset)
            params = {'access_token': cfg.token, 'v': 5.131, 'group_id': group_id, 'offset': offset * 1000,
                      'fields': 'bdate, city, country, schools, sex, universities'}
            users = requests.get('https://api.vk.com/method/groups.getMembers', params=params).json()['response']
            
            for user in users['items']:
                if 'deactivated' in user or user['first_name'] == 'deleted':
                    continue
                record = [user.get('id'), user.get('first_name'), user.get('last_name'), user.get('bdate'),
                          user.get('city', {}).get('title') if user.get('city') else None,
                          user.get('country', {}).get('title') if user.get('country') else None,
                          user.get('schools', [{}])[0].get('name') if user.get('schools') else None,
                          user.get('sex'),
                          user.get('universities', [{}])[0].get('name') if user.get('universities') else None
                          ]
                writer.writerow(record)
                
