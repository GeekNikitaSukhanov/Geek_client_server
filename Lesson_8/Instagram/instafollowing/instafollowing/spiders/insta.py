import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from Instagram.instafollowing.instafollowing.items import InstafollowingItem, InstafollowingItem_2


class InstaSpider(scrapy.Spider):
    name = 'insta'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    insta_login_url = 'https://www.instagram.com/accounts/login/ajax/'
    insta_login = 'venskiy'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1631267076:AbNQAGVdgk5afXEo6HAmtqGzSkoEaea67NtzJaMXILLOrO0jOtd/VrebZM3WokXAI0RZ49pT8nZCX4pzFkh4jIaliGExL9C+XKO8w4DM4cro7TFex0GtKQxkBgc8fVEgy6BuaOAuQzDP7YVkTh9C0ybb'
    user_parse_2 = 'buzzfeedtasty'
    user_parse_1 = '9gag'
    followers_url = 'https://i.instagram.com/api/v1/friendships/'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_url,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pwd},
                                 headers={'x-csrftoken': csrf})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(f'/{self.user_parse_1}',
                                  callback=self.request_followers,
                                  cb_kwargs={'username': self.user_parse_1})

    def request_followers(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'count': 12, 'search_surface': 'follow_list_page'}
        followers_url = f'{self.followers_url}{user_id}/followers/?{urlencode(variables)}'

        yield response.follow(followers_url, callback=self.followers_data_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)},
                              headers={'USER-AGENT': 'Instagram 155.0.0.37.107'})

    def followers_data_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data['next_max_id']:
            variables['max_id'] = j_data['next_max_id']
            followers_url = f'{self.followers_url}{user_id}/followers/?{urlencode(variables)}'

            yield response.follow(followers_url, callback=self.request_following,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)},
                                  headers={'USER-AGENT': 'Instagram 155.0.0.37.107'})
            users = j_data.get('users')
            for user in users:
                item = InstafollowingItem(account_id=user_id,
                                          account_name=username,
                                          follower_id=user.get('pk'),
                                          follower_name=user.get('username'),
                                          follower_photo=user.get('profile_pic_url'))
                yield item

    def request_following(self, response: HtmlResponse, username, user_id, variables):
        variables = {'count': 12}
        following_url = f'{self.followers_url}{user_id}/following/?{urlencode(variables)}'

        yield response.follow(following_url, callback=self.following_data_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)},
                              headers={'USER-AGENT': 'Instagram 155.0.0.37.107'})

    def following_data_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data['next_max_id']:
            variables['max_id'] = j_data['next_max_id']
            following_url = f'{self.followers_url}{user_id}/following/?{urlencode(variables)}'

            yield response.follow(following_url, callback=self.login_2,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)},
                                  headers={'USER-AGENT': 'Instagram 155.0.0.37.107'})
            users = j_data.get('users')
            for user in users:
                item_2 = InstafollowingItem_2(account_id=user_id,
                                              account_name=username,
                                              following_id=user.get('pk'),
                                              following_name=user.get('username'),
                                              following_photo=user.get('profile_pic_url'))
                yield item_2

    def login_2(self, response: HtmlResponse):
        yield response.follow(f'/{self.user_parse_2}',
                              callback=self.request_followers_2,
                              cb_kwargs={'username': self.user_parse_2})

    def request_followers_2(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'count': 12, 'search_surface': 'follow_list_page'}
        followers_url = f'{self.followers_url}{user_id}/followers/?{urlencode(variables)}'

        yield response.follow(followers_url, callback=self.followers_data_parse_2,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)},
                              headers={'USER-AGENT': 'Instagram 155.0.0.37.107'})

    def followers_data_parse_2(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data['next_max_id']:
            variables['max_id'] = j_data['next_max_id']
            followers_url = f'{self.followers_url}{user_id}/followers/?{urlencode(variables)}'

            yield response.follow(followers_url, callback=self.request_following_2,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)},
                                  headers={'USER-AGENT': 'Instagram 155.0.0.37.107'})
            users = j_data.get('users')
            for user in users:
                item = InstafollowingItem(account_id=user_id,
                                          account_name=username,
                                          follower_id=user.get('pk'),
                                          follower_name=user.get('username'),
                                          follower_photo=user.get('profile_pic_url'))
                yield item

    def request_following_2(self, response: HtmlResponse, username, user_id, variables):
        variables = {'count': 12}
        following_url = f'{self.followers_url}{user_id}/following/?{urlencode(variables)}'

        yield response.follow(following_url, callback=self.following_data_parse_2,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)},
                              headers={'USER-AGENT': 'Instagram 155.0.0.37.107'})

    def following_data_parse_2(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data['next_max_id']:
            variables['max_id'] = j_data['next_max_id']
            following_url = f'{self.followers_url}{user_id}/following/?{urlencode(variables)}'

            yield response.follow(following_url, callback=self.following_data_parse_2(),
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)},
                                  headers={'USER-AGENT': 'Instagram 155.0.0.37.107'})
            users = j_data.get('users')
            for user in users:
                item_2 = InstafollowingItem_2(account_id=user_id,
                                              account_name=username,
                                              following_id=user.get('pk'),
                                              following_name=user.get('username'),
                                              following_photo=user.get('profile_pic_url'))
                yield item_2

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched).get('id')
