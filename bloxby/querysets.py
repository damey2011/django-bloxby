from django.db import models

from .functions import Bloxby

bloxby = Bloxby()


class UserBridgeQuerySet(models.QuerySet):
    def create(self, **kwargs):
        if not kwargs.pop('override'):
            raise Exception('Use UserBridge.create(bloxby_package_id, django_user) instead.')
        return super(UserBridgeQuerySet, self).create(**kwargs)

    def delete(self):
        qs = self._chain()
        for item in qs:
            # This calls the model delete for each, might not be query efficient, but this is what we want
            item.delete()
