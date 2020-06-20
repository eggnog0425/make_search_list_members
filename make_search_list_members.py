from requests_oauthlib import OAuth1Session
import os
import json
import configparser

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')

end_point = config_ini['end_point']['list_members']

# OAUTH認証
consumer_key = config_ini['consumer']['key']
consumer_secret = config_ini['consumer']['secret']
access_token = config_ini['access']['token']
access_secret = config_ini['access']['secret']

twitter = OAuth1Session(consumer_key, consumer_secret,
                        access_token, access_secret)

# GETパラメータの生成
params = {'list_id': config_ini['get_parameters']['list_id'],
          'count': config_ini['get_parameters']['count']}
response = twitter.get(end_point, params=params)

if response.status_code != 200:
    print('getlist members failed!!')
    os._exit(1)

members = response.json()['users']

search_word = ''
first = True
for member in members:
    add_word = '{}from:{}'
    if first:
        search_word += add_word.format('', member['screen_name'])
        first = False
        continue

    add_word = add_word.format(' OR ', member['screen_name'])
    length = len(search_word + add_word)
    if int(config_ini['search_word']['max_length']) < length:
        print('search word is too long!!!!')
        break
    search_word += add_word

with open(config_ini['output_file']['path'], mode='w') as f:
    f.write(search_word)
