from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from fingerprint import views, views_login, views_admin

urlpatterns = patterns('',
    url(r'^accounts/login/$', views_login.login, name='login'),
    url(r'^accounts/auth/$', views_login.auth_view, name='auth'),
    url(r'^accounts/logout/$', views_login.logout, name='logout'),
    url(r'^accounts/registration/$', views_login.registration, name='registration'),
    url(r'^accounts/registrate/$', views_login.registrate_user, name='registrate'),
    url(r'^accounts/loggedin/$', views_login.loggedin, name='loggedin'),
    url(r'^accounts/invalid/$', views_login.invalid_login, name='invalid_login'),

    url(r'^$', RedirectView.as_view(url='/fingerprint/home_user/')),
    url(r'^home_user/$', views.home_user, name='home_user'),
    url(r'^doors_user/$', views.doors_user, name='doors_user'),
    url(r'^profile_user/$', views.profile_user, name='profile_user'),
    url(r'^save_profile_changes/$', views.save_profile_changes, name='save_profile_changes'),
    url(r'^fingerprint_user/$', views.fingerprint_user, name='fingerprint_user'),
    url(r'^fingerprint_enrollment/$', views.start_enrollment, name='enrollment'),

    url(r'^home_admin/$', views_admin.home_admin, name='home_admin'),
    url(r'^users_admin/$', views_admin.users_admin, name='users_admin'),
    url(r'^users_admin/(?P<user_id>\d+)/$', views_admin.edit_user_admin, name='edit_user_admin'),
    url(r'^save_admin_user_changes/(?P<user_id>\d+)/$', views_admin.save_admin_user_changes, name='save_admin_user_changes'),
    url(r'^doors_admin/$', views_admin.doors_admin, name='doors_admin'),
    url(r'^add_door_admin/$', views_admin.add_door_admin, name='add_door_admin'),
    url(r'^doors_admin/(?P<door_id>\d+)/$', views_admin.edit_door_admin, name='edit_door_admin'),
    url(r'^save_admin_door_changes/(?P<door_id>\d+)/$', views_admin.save_admin_door_changes, name='save_admin_door_changes'),
)