# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/admin')),
    path('admin/', admin.site.urls),
    path('bloxby/', include('djbloxby.bloxby.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
