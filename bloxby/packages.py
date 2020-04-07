import json

import requests
from .generics import Generic


class Package(Generic):
    path = '/api/packages/'

    def create(
        self, name, sites_number=20, hosting_option=None, price=0, subscription='Monthly', currency='USD',
        export_site=True, ftp_publish=True, disk_space=100, templates=None, blocks=None, status='Active'
    ):
        if not hosting_option:
            hosting_option = [
                'Sub-Folder'
            ]
        data = [
            ('name', f'{self.package_prefix}{name}'),
            ('sites_number',  sites_number),
            ('price', price),
            ('subscription', subscription),
            ('currency', currency),
            ('export_site', self.bool_cast(export_site)),
            ('ftp_publish', self.bool_cast(ftp_publish)),
            ('disk_space', disk_space),
            ('status', status)
        ]
        if templates:
            data.append(('templates', json.dumps(templates)))
        if blocks:
            data.append(('blocks', json.dumps(blocks)))
        if hosting_option:
            data.append(('hosting_option', json.dumps(hosting_option)))
        response = requests.post(
            f'{self.base_url}{self.path}', data=data, headers=self.get_headers(), auth=(self.get_auth())
        )
        return response.json(), response.status_code in [200, 201]

    def update(self, package_id, **kwargs):
        response = requests.put(
            f'{self.base_url}{self.path}{package_id}/', data=kwargs, headers=self.get_headers(), auth=self.get_auth()
        )
        return response.json(), response.status_code in [201, 200]

    def delete(self, package_id):
        response = requests.delete(
            f'{self.base_url}{self.path}{package_id}/', headers=self.get_headers(), auth=self.get_auth()
        )
        return response.status_code == 204

    def retrieve(self, package_id):
        response = requests.get(
            f'{self.base_url}{self.path}{package_id}/', headers=self.get_headers(), auth=self.get_auth()
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
