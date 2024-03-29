import requests
import time
import json


class VkApi:

    TOKEN = '7a0661dca1f121bc42890e9704f37a05b56bf11d333ebe96f6b8a4bf76e646add99fa5282fb1d9fe38891'
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

    def get_response(self, params, method_url):
        response = requests.get(
            method_url,
            params=params
        )
        result = response.json()
        if 'error' in result:
            raise Exception(result)
        else:
            return result

    def get_friends(self, user_id):
        params = self.get_general_params()
        params['user_id'] = user_id
        result = self.get_response(params, 'https://api.vk.com/method/friends.get')
        friends_id_list = result['response']['items']
        new_list_friends = []
        for id in friends_id_list:
            new_user = VkUser(id)
            new_list_friends.append(new_user)
        return new_list_friends

    def get_subscriptions(self, user_id):
        params = self.get_group_params(1, 'members_count')
        params['user_id'] = user_id
        result = self.get_response(params, 'https://api.vk.com/method/users.getSubscriptions')
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
        result = self.get_response(params, 'https://api.vk.com/method/users.get')
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
        if len(self.subscriptions) == 0:
            self.get_subscriptions_from_api(api_obj)
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
    program_active = True
    while program_active:
        print(
            '\n→ Введите ID / имя пользователя. Если хотите выйти из программы, введите exit: '
        )
        user_input = input()
        if user_input == "exit":
            program_active = False
        else:
            my_api = VkApi()
            try:
                my_user = VkUser.from_dict(my_api.get_user(user_input))
                my_user.compare_groups(my_api)
            except Exception as e:
                print('При выполнении возникла ошибка: ', e)
    if not program_active:
        print('→ Спасибо за использование нашей программы!')


main()