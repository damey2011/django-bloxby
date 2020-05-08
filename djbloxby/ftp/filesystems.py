import os

from pyftpdlib.filesystems import AbstractedFS

from django.conf import settings


class CustomFileSystem(AbstractedFS):
    def __init__(self, root, cmd_channel):
        root_path = settings.TMP
        if not os.path.exists(root_path):
            os.mkdir(root_path)
        root_path = os.path.join(root_path, cmd_channel.user_home)
        if not os.path.exists(root_path):
            os.mkdir(root_path)
        super(CustomFileSystem, self).__init__(root_path, cmd_channel)
