import requests

from .generics import Generic


class User(Generic):
    path = '/api/users/'

    def create(self, first_name, last_name, email, password, package_id=None, type_='User'):
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': f'{self.account_email_prefix}{email}',
            'password': password,
            'type': type_,
            'package_id': package_id
        }
        response = requests.post(
            f'{self.base_url}{self.path}', data=data, headers=self.get_headers(), auth=self.get_auth()
        )
        return response.json(), response.status_code in [200, 201]

    def update(self, user_id, **kwargs):
        response = requests.put(
            f'{self.base_url}{self.path}{user_id}/', data=kwargs, headers=self.get_headers(), auth=self.get_auth()
        )
        return response.json(), response.status_code in [201, 200]

    def delete(self, user_id):
        response = requests.delete(
            f'{self.base_url}{self.path}{user_id}/', headers=self.get_headers(), auth=self.get_auth()
        )
        return response.status_code == 204

    def retrieve(self, user_id):
        response = requests.get(
            f'{self.base_url}{self.path}{user_id}/', headers=self.get_headers(), auth=self.get_auth()
        )
        data = response.json()
        is_success = response.status_code == 200
        return data[0] if is_success else data, is_success

    def all(self):
        response = requests.get(
            f'{self.base_url}{self.path}/', headers=self.get_headers(), auth=self.get_auth()
        )
        data = response.json()
        is_success = response.status_code == 200
        return data if is_success else data, is_success
