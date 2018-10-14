from django.conf.urls import url

from . import views
from . import api

app_name = 'explorer'

urlpatterns = [
    url(r'^api/test$', api.test, name='test'),
    url(r'^api/accounts$', api.accounts, name='accounts'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^index$', views.index, name='index'),
    url(r'^accounts/list$', views.list_accounts, name='list_accounts'),
    url(r'^accounts/add$', views.add_account, name='add_account'),
    url(r'^accounts/(?P<account_id>\d+)/telegram_sign_in/(?P<telegram_phone_hash>[a-zA-Z0-9_]+)$', views.telegram_sign_in, name='telegram_sign_in'),
    url(r'^accounts/(?P<account_id>\d+)/remote_chats/list$', views.list_remote_chats, name='list_remote_chats'),
    url(r'^accounts/(?P<account_id>\d+)/remote_chats/add/(?P<remote_id>\d+)_(?P<remote_type>\d+)$', views.import_remote_chat, name='import_remote_chat'),
    url(r'^chats/explore/(?P<chat_id>\d+)$', views.explore_chat, name='explore_chat'),
    url(r'^$', views.index, name='index'),
]
