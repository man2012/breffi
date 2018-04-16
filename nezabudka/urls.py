from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.ContactsListView.as_view(), name='contacts'),
    url(r'^create$', views.ContactCreateView.as_view(), name='contacts_create'),
    url(r'^edit/(?P<pk>[0-9]+)$', views.ContactUpdateView.as_view(), name='contacts_edit'),
    url(r'^delete/(?P<pk>[0-9]+)$', views.ContactDeleteView.as_view(), name='contacts_delete'),
    url(r'^detail/(?P<pk>[0-9]+)$', views.ContactDetailView.as_view(), name='contacts_detail'),
    url(r'^export/json$', views.export_json, name='export_json'),
    url(r'^import/json$', views.FileUploadView.as_view(), name='import_json'),
    url(r'^import/json/site$', views.import_json_site, name='import_json_site'),
    url(r'^api$', views.ContactList.as_view(), name='myapi'),
    url(r'^api/(?P<pk>[0-9]+)/$', views.ContactDetail.as_view()),
]
