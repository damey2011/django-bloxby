from django.db.models import Manager


class UserBridgeManager(Manager):
    def all(self):
        return super(UserBridgeManager, self).all().filter(active=True)

    def create(self, **kwargs):
        raise Exception('Use UserBridge.create(bloxby_package_id, django_user) instead.')
