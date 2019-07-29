import requests
import time
import json

user_id_input = input('Введите ID пользователя: ')

class VkApi:

    TOKEN = '969ac6f94358deeb40764bedfb343e81ddeb55b3c2e84f4450b84efc83c62d1ed27468969943be4e49eec'
    Version = '5.52'

    def get_general_params(self):
        return {
            'access_token': self.TOKEN,
            'v': self.Version
        }

    def get_group_params(self, is_extended, req_fields):
        return {
            'access_token': self.TOKEN,
            'v': self.Version,
            'extended': is_extended,
            'fields': req_fields
        }

    def get_friends(self, user_id):
        params = self.get_general_params()
        params['user_id'] = user_id
        response = requests.get(
            'https://api.vk.com/method/friends.get',
            params=params
        )
        result = response.json()
        friends_id_list = result['response']['items']
        new_list_friends = []
        for id in friends_id_list:
            new_user = VkUser(id)
            new_list_friends.append(new_user)
        return new_list_friends

    def get_subscriptions(self, user_id):
        params = self.get_group_params(1, 'members_count')
        params['user_id'] = user_id
        response = requests.get(
            'https://api.vk.com/method/users.getSubscriptions',
            params=params
        )
        result = response.json()
        new_list_groups = []
        try:
            if result['response']['items'] is not []:
                groups_list = result['response']['items']
                for group in groups_list:
                    new_group = VkGroup(group['id'], group['name'], group['members_count'])
                    new_list_groups.append(new_group)
        except KeyError:
            pass
        return new_list_groups

    def get_users(self, user_ids):
        params = self.get_general_params()
        params['user_ids'] = user_ids
        response = requests.get(
            'https://api.vk.com/method/users.get',
            params=params
        )
        result = response.json()
        return result['response']

    def get_user(self, user_credential):
        if ',' in user_credential:
            raise Exception('Ошибка ввода: параметр не должен содержать запятую')
        if 'А-я' in user_credential:
            raise Exception(
                'Ошибка ввода: параметр должен содержать только\
                 латинские символы или цифры'
            )
        users_list = self.get_users(user_credential)
        if len(users_list) != 1:
            raise Exception('Получено более 1 пользователя')
        return users_list[0]


class VkUser:
    def __init__(self, user_id):
        self.gid = user_id
        self.friends = list()
        self.subscriptions = list()

    @classmethod
    def from_dict(cls, my_dict):
        return cls(my_dict['id'])

    def get_friends_from_api(self, api_obj):
        self.friends = api_obj.get_friends(self.gid)

    def get_subscriptions_from_api(self, api_obj):
        self.subscriptions = api_obj.get_subscriptions(self.gid)

    def get_friends_subscriptions(self, api_obj):
        friends_groups = set()
        for user in self.friends:
            try:
                user.get_subscriptions_from_api(api_obj)
                friends_groups.update(user.subscriptions)
                print('---Ожидание---')
            except requests.exceptions.ReadTimeout:
                continue
            time.sleep(0.01)
        return friends_groups

    def compare_groups(self, api_obj):
        user_groups = self.subscriptions
        friends_groups = self.get_friends_subscriptions(api_obj)
        result = list(set(user_groups) - set(friends_groups))
        json_string = json.dumps(
                        [ob.__dict__ for ob in result],
                        sort_keys=False,
                        indent=4,
                        ensure_ascii=False,
                        separators=(',', ': '))
        print(json_string)
        with open('groups.json', 'w+', encoding='utf-8') as f:
            json.dump(json_string, f, sort_keys=False,
                      indent=4,
                      ensure_ascii=False,
                      separators=(',', ': '))


class VkGroup:
    def __init__(self, group_id, name, members_count):
        self.group_id = group_id
        self.members_count = members_count
        self.name = name

    def __eq__(self, gr_2):
        return self.group_id == gr_2.group_id

    def __hash__(self):
        return self.group_id


def main():

    my_api = VkApi()
    my_user = VkUser.from_dict(my_api.get_user(user_id_input))
    my_user.get_friends_from_api(my_api)
    my_user.get_subscriptions_from_api(my_api)
    my_user.get_friends_subscriptions(my_api)
    my_user.compare_groups(my_api)

main()

