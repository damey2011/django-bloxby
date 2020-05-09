from django.contrib import admin

from .models import UserBridge, Template, TemplateAsset, Page

admin.site.register(UserBridge)
admin.site.register(Template)
admin.site.register(TemplateAsset)
admin.site.register(Page)
