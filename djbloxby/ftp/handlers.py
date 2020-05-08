import os

import requests
from django.conf import settings
from pyftpdlib.handlers import FTPHandler


class Handler(FTPHandler):
    def send_archive(self, archive_file):
        """Execute the API request to the collector here"""
        print(f'Sent {archive_file} to server.')

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_login(self, username):
        pass

    def on_logout(self, username):
        # do something when user logs out
        print('logged out')
        pass

    def on_file_sent(self, file):
        # do something when a file has been sent
        pass

    def on_file_received(self, file):
        pre_path = os.path.join(settings.TMP_UPLOADS_DIR, self.user_home)
        application = self.application
        rel_file_path = file.replace(pre_path, '').lstrip('/')
        with open(file, 'rb') as f:
            resp = requests.post(application.receiving_url, {
                'target': self.target, 'obj_id': self.obj_id, 'user_bloxby_id': self.user
            }, files={
                rel_file_path: (rel_file_path, f.read())
            })

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        print('Inc ' + file)
