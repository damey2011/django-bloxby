from django.db.models import Manager

from .querysets import UserBridgeQuerySet


class UserBridgeManager(Manager):
    def get_queryset(self):
        return UserBridgeQuerySet(self.model, using=self._db).filter(active=True)

    def everything(self):
        return super(UserBridgeManager, self).get_queryset()
