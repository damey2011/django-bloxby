from django.conf import settings
from django.db import models

from .managers import UserBridgeManager
from .functions import Bloxby

bloxby = Bloxby()


class UserBridge(models.Model):
    """You can create this at post_save of PurchasedPackage or something similar, a model that represents that the user
    has purchased a package, and delete it also at post_delete"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bloxby_id = models.IntegerField(blank=True, null=True)
    autologin_token = models.CharField(max_length=20, blank=True, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = UserBridgeManager()

    def __str__(self):
        return f'{self.user.email} - {self.bloxby_id}'

    def delete(self, using=None, keep_parents=False):
        bloxby.Users.update(self.bloxby_id, status='Inactive')
        self.active = False
        self.save()

    @classmethod
    def create(cls, package_id, user):
        """
        Package_id is the bloxby package id not the internal one
        Simply call UserBridge.create(package_id, user);
        """
        # Check if user already exists in bloxby
        existings = cls.objects.filter(user=user)
        if existings.exists():
            obj = existings.first()
            obj.active = True
            obj.save()
            new = obj
            bloxby.Users.update(obj.bloxby_id, status='Active')
        else:
            # Check if email already exists there
            new = cls.objects.create(user=user)
            data, _ = bloxby.Users.create(
                user.first_name, user.last_name, user.email, bloxby.generate_random_password(), package_id
            )
            new.bloxby_id = data['data']['user']['id']
            new.save()
        return new
