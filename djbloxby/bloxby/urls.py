from django.urls import path

from djbloxby.bloxby import views

urlpatterns = [
    path('ftp/receive/', views.ReceiveFTPItemsView.as_view(), name='receive'),
    path('ftp/auth/', views.AuthFTPUserView.as_view(), name='auth'),
    path('page/', views.PageRenderView.as_view(), name='render-page')
]
