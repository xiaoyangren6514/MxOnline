from django.conf.urls import url, include

from organization.views import OrgView

urlpatterns = [
    url(r'^list/', OrgView.as_view(), name='org_list'),
]
