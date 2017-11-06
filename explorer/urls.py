from django.conf.urls import url

from . import views

app_name = 'explorer'

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^index$', views.index, name='index'),
    url(r'^chat/accounts$', views.list_chat_accounts, name='list_chat_accounts'),
    url(r'^chat/add$', views.add_chat_account, name='add_chat_account'),
    url(r'^chat/telegram_sign_in/(?P<chat_account_id>[0-9]+)/(?P<telegram_phone_hash>[0-9]+)$', views.telegram_sign_in, name='telegram_sign_in'),
    url(r'^chat/(?P<chat_account_id>\d+)/channels$', views.list_chat_channels, name='list_chat_channels'),
    url(r'^chat/(?P<chat_account_id>\d+)/save_channel/(?P<remote_type>\d+)/(?P<remote_id>\d+)$', views.save_channel, name='save_channel'),
    url(r'^$', views.index, name='index'),
]
