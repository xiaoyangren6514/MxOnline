from django.conf.urls import url

from users.views import UserCenterView, UserUploadImageView

urlpatterns = [
    url(r'^info/$', UserCenterView.as_view(), name='user_info'),
    url(r'^image/upload/$', UserUploadImageView.as_view(), name='user_image_upload'),
]
