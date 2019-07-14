import requests

TOKEN = '150e9e6ced3fb222ecd7c123d7706e1499e5b2bc255b82d3d61cb6d7ec2731e33fc5cea08549e5ef78aa9'


class VkUser:
    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def get_params(self):
        return {
            'access_token': self.token,
            'v': '5.52'
        }

    def request(self, method, params):
        response = requests.get(
            'https://api.vk.com/method/' + method,
            params=params
        )
        return response

    def get_friends(self):
        params = self.get_params()
        params['user_id'] = self.user_id
        response = requests.get(
            'https://api.vk.com/method/friends.get',
            params=params
        )
        result = response.json()
        initial_list = result['response']
        id_list = initial_list['items']
        new_list = []
        for id in id_list:
            new_user = VkUser(TOKEN, id)
            new_list.append(new_user)
        return new_list

    def __and__(self, user_2):
        friends_list_1 = self.get_friends()
        friends_list_2 = user_2.get_friends()
        result = list(set(friends_list_1) & set(friends_list_2))
        return result

    def __eq__(self, user_2):
        return self.user_id == user_2.user_id

    def __hash__(self):
        return self.user_id


user_1 = VkUser(TOKEN, 6228250)
user_2 = VkUser(TOKEN, 585956)
cross = user_1 & user_2
print('Количество общих друзей:', len(cross))


