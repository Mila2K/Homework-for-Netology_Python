import requests
import time
import json

TOKEN = '2db033ddb29ece88be054fe12d44f8e1327023a915fc222043832fa83215d6662b0580e11d93c834c1067'


class VkSubscription:
    def __init__(self, user_id):
        self.name = ''
        self.gid = user_id
        self.members_count = 0

    def fill_fields(self, name, members_count):
        self.name = name
        self.members_count = members_count

    def get_general_params(self):
        return {
            'access_token': TOKEN,
            'v': '5.52'
        }

    def get_group_params(self):
        return {
            'access_token': TOKEN,
            'v': '5.52',
            'extended': 1,
            'fields': 'members_count'
        }

    def request(self, method, params):
        response = requests.get(
            'https://api.vk.com/method/' + method,
            params=params
        )
        return response

    def get_groups(self):
        params = self.get_group_params()
        params['user_id'] = self.gid
        response = requests.get(
            'https://api.vk.com/method/users.getSubscriptions',
            params=params
        )
        result = response.json()
        groups_list = result['response']['items']
        new_list_groups = []
        for group in groups_list:
            new_group = VkSubscription(group['id'])
            new_group.fill_fields(group['name'], group['members_count'])
            new_list_groups.append(new_group)
            print(group['id'])
        return new_list_groups

    def get_friends(self):
        params = self.get_general_params()
        params['user_id'] = self.gid
        response = requests.get(
            'https://api.vk.com/method/friends.get',
            params=params
        )
        result = response.json()
        friends_id_list = result['response']['items']
        new_list_friends = []
        for id in friends_id_list:
            new_user = VkSubscription(id)
            new_list_friends.append(new_user)
        return new_list_friends

    def get_friends_groups(self):
        result_groups = []
        new_list_friends = self.get_friends()
        for friend in new_list_friends:
            params = friend.get_group_params()
            params['user_id'] = friend.gid
            print('\n', friend.gid)
            response = requests.get(
                'https://api.vk.com/method/users.getSubscriptions',
                params=params
            )
            result = response.json()
            friends_groups = []
            try:
                if result['response']['items'] is not []:
                    groups_id_list = result['response']['items']
                    for group in groups_id_list:
                        new_group = VkSubscription(group['id'])
                        new_group.fill_fields(group['name'], group['members_count'])
                        friends_groups.append(new_group)
            except KeyError:
                print('Нет доступа к аккаунту пользователя!')
                continue
            except requests.exceptions.ReadTimeout:
                continue
            result_groups.extend(friends_groups)
            print('--- Ожидание ---')
            time.sleep(0.01)
        return result_groups

    def compare_groups(self):
        user_groups = self.get_groups()
        friends_groups = self.get_friends_groups()
        result = list(set(user_groups) - set(friends_groups))
        json_string = json\
            .dumps(
            [ob.__dict__ for ob in result],
            sort_keys=False,
            indent=4,
            ensure_ascii=False,
            separators=(',', ': '))
        print(json_string)

    def __eq__(self, user_2):
        return self.gid == user_2.gid

    def __hash__(self):
        return self.gid


users = VkSubscription(585956)
# users.get_groups()
# users.get_friends()
users.compare_groups()
# users.get_friends_groups()

