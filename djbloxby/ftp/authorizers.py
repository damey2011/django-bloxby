import requests
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed

from djbloxby.ftp.models import Application


class APIAuth(DummyAuthorizer):
    """
    Authentication is in the format:
    username: app_name|bloxby_auth_id|target|obj_id
    password: user_password
    # Target could be 'home, event'
    # Object id carries the id of the event, if it's a home page to an event, otherwise 'null'
    """
    def validate_authentication(self, username, password, handler):
        msg = 'Authentication Failed'
        app_and_username_and_target = username.lower().split('|')
        app_name = app_and_username_and_target[0]
        username = app_and_username_and_target[1]
        target = app_and_username_and_target[2]
        obj_id = app_and_username_and_target[3]
        try:
            # Meta is going to be anything that will assist us in identifying the target
            application = Application.objects.get(name__iexact=app_name)
        except Application.DoesNotExist:
            raise AuthenticationFailed(msg)
        response = requests.post(application.auth_url, data={'username': username, 'password': password})
        if 199 < response.status_code < 300:
            setattr(handler, 'target', target)
            setattr(handler, 'user', username)
            setattr(handler, 'obj_id', obj_id)
            setattr(handler, 'application', application)
            setattr(handler, 'user_home', str(app_name) + str(username) + str(target))
            return None
        raise AuthenticationFailed(msg)

    def get_msg_login(self, username):
        return f'Welcome {username}'

    def has_user(self, username):
        return True

    def get_home_dir(self, username):
        return ''

    def has_perm(self, username, perm, path=None):
        return perm in self.get_perms(username)

    def get_perms(self, username):
        return 'mwaler'
