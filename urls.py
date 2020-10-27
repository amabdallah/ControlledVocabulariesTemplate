from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
#from cvinterface.views.base_views import UnitsListView

from cvservices.api import v1_api

from cvinterface.controlled_vocabularies import requests
from cvinterface.views.vocabulary_views import VocabulariesView, list_views, detail_views
from cvinterface.views.request_views import RequestsView, \
    request_list_views, request_create_views, request_update_views

login_configuration = {
    'template_name': 'cvinterface/account/login.html',
    'redirect_field_name': 'next'
}

logout_configuration = {
    'next_page': reverse_lazy('home')
}

urlpatterns = [
    url(r'^' + settings.SITE_URL + '$', VocabulariesView.as_view(), name='home'),
    url(r'^' + settings.SITE_URL + 'api/', include(v1_api.urls)),
    url(r'^' + settings.SITE_URL + 'admin/', include(admin.site.urls)),
    #url(r'^' + settings.SITE_URL + 'units/', UnitsListView.as_view(), name='units'),
    url(r'^' + settings.SITE_URL + 'requests/$', RequestsView.as_view(), name='requests_list'),
    url(r'^' + settings.SITE_URL + 'login/$', auth_views.login, login_configuration, name='login'),
    url(r'^' + settings.SITE_URL + 'logout/$', auth_views.logout, logout_configuration, name='logout'),
]


# cv list views
for cv_name in list_views:
    view = list_views[cv_name]

    urlpatterns += [
        url(r'^' + settings.SITE_URL + cv_name + '/$', view, name=cv_name),
    ]

# cv detail views
for cv_name in detail_views:
    view = detail_views[cv_name]

    urlpatterns += [
        url(r'^' + settings.SITE_URL + cv_name + '/(?P<slug>[-\w]+)/(?P<pk>[-\w]+)/$', view, name=cv_name + '_detail'),
    ]
    urlpatterns += [
        url(r'^' + settings.SITE_URL + cv_name + '/(?P<slug>[-\w]+)/$', view, name=cv_name + '_detail'),
    ]


# request list views
for request_name in request_list_views:
    view = request_list_views[request_name]

    urlpatterns += [
        url(r'^' + settings.SITE_URL + 'requests/' + requests[request_name]['vocabulary'] + '/$', view,
            name=request_name),
    ]

# request create views
for request_name in request_create_views:
    view = request_create_views[request_name]
    urlpatterns += [
        url(r'^' + settings.SITE_URL + 'requests/' + requests[request_name]['vocabulary'] + '/new/$', view,
            name=requests[request_name]['vocabulary'] + '_form'),
        url(r'^' + settings.SITE_URL + 'requests/' + requests[request_name]['vocabulary'] + '/new/(?P<vocabulary_id>[\w]+)/$',
            view, name=requests[request_name]['vocabulary'] + '_form'),
    ]

# request update views
for request_name in request_update_views:
    view = request_update_views[request_name]

    urlpatterns += [
        url(r'^' + settings.SITE_URL + 'requests/' + requests[request_name]['vocabulary'] + '/(?P<pk>[-\w]+)/$', view,
            name=requests[request_name]['vocabulary'] + '_update_form'),
    ]
