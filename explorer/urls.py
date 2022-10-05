from django.urls import re_path

from . import views

app_name = 'explorer'

urlpatterns = [
    re_path(r'^login$', views.login, name='login'),
    re_path(r'^logout$', views.logout, name='logout'),
    re_path(r'^index$', views.index, name='index'),
    re_path(r'^accounts/list$', views.list_accounts, name='list_accounts'),
    re_path(r'^accounts/add$', views.add_account, name='add_account'),
    re_path(r'^accounts/(?P<account_id>\d+)/telegram_sign_in/(?P<telegram_phone_hash>[a-zA-Z0-9_]+)$', views.telegram_sign_in, name='telegram_sign_in'),
    re_path(r'^accounts/(?P<account_id>\d+)/remote_chats/list$', views.list_remote_chats, name='list_remote_chats'),
    re_path(r'^accounts/(?P<account_id>\d+)/remote_chats/add/(?P<remote_id>\d+)_(?P<remote_type>\d+)$', views.import_remote_chat, name='import_remote_chat'),
    re_path(r'^chats/(?P<chat_id>\d+)/explore$', views.explore_chat, name='explore_chat'),
    re_path(r'^chats/(?P<chat_id>\d+)/change_author_role$', views.change_author_role, name='change_author_role'),
    re_path(r'^$', views.index, name='index'),
]
