class Generic:
    def __init__(self, base_url, username, password, package_prefix, public_key, account_email_prefix):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.package_prefix = package_prefix
        self.account_email_prefix = account_email_prefix
        self.public_key = public_key

    @staticmethod
    def bool_cast(b):
        return 'yes' if b else 'no'

    def get_auth(self):
        return self.username, self.password

    def get_headers(self):
        return {
            'X-API-KEY': self.public_key,
        }

    def create(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass

    def retrieve(self, **kwargs):
        pass
