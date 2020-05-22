from django import template
from django.conf import settings

from ..models import UserBridge

register = template.Library()


@register.simple_tag(takes_context=True)
def user_builder_dashboard(context):
    user = context['request'].user
    try:
        if user.is_authenticated:
            userbridge = UserBridge.objects.get(user=user)
            if userbridge.bloxby_id:
                return user.userbridge.dashboard_url
    except UserBridge.DoesNotExist:
        # Never mind
        pass
    return UserBridge.create(user).dashboard_url


@register.simple_tag
def builder_create_site():
    return f"{settings.BLOXBY_BUILDER['url']}/sites/create"
