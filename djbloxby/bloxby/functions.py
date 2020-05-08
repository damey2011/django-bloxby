import hashlib
import random
import string

from django.conf import settings

from .users import User
from .packages import Package

BASE_URL = settings.BLOXBY_BUILDER['url']
USERNAME = settings.BLOXBY_BUILDER['username']
PASSWORD = settings.BLOXBY_BUILDER['password']
PACKAGE_PREFIX = settings.BLOXBY_BUILDER['package_prefix']
ACCOUNT_EMAIL_PREFIX = settings.BLOXBY_BUILDER['account_email_prefix']
PUBLIC_KEY = settings.BLOXBY_BUILDER['public_key']
AUTOLOGIN_HASH = settings.BLOXBY_BUILDER['autologin_hash']


class Bloxby:
    Users = User(BASE_URL, USERNAME, PASSWORD, PACKAGE_PREFIX, PUBLIC_KEY,ACCOUNT_EMAIL_PREFIX)
    Packages = Package(BASE_URL, USERNAME, PASSWORD, PACKAGE_PREFIX, PUBLIC_KEY, ACCOUNT_EMAIL_PREFIX)

    @staticmethod
    def generate_login_hash():
        return hashlib.md5(f'{BASE_URL}/{AUTOLOGIN_HASH}'.encode('utf-8')).hexdigest()

    @staticmethod
    def generate_random_password():
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(15))
