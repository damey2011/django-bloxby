from django import template

from ..models import UserBridge

register = template.Library()


@register.simple_tag(takes_context=True)
def user_builder_dashboard(context):
    user = context['request'].user
    try:
        if user.is_authenticated and user.userbridge.bloxby_id:
            return user.userbridge.dashboard_url
    except UserBridge.DoesNotExist:
        pass
    return '#'
