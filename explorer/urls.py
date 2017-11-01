from django.conf.urls import url

from . import views

app_name = 'explorer'

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^telegram_sign_in$', views.telegram_sign_in, name='telegram_sign_in'),
    url(r'^$', views.index, name='index'),
]
