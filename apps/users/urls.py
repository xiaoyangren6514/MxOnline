from django.conf.urls import url

from users.views import UserCenterView, UserUploadImageView, UserModifyPwd, UpdateEmailView, UpdateEmailVerifyView

urlpatterns = [
    url(r'^info/$', UserCenterView.as_view(), name='user_info'),
    url(r'^image/upload/$', UserUploadImageView.as_view(), name='user_image_upload'),
    url(r'^modify/pwd/$', UserModifyPwd.as_view(), name='user_modify_pwd'),
    url(r'^update/email/$', UpdateEmailView.as_view(), name='user_update_email'),
    url(r'^update/email/verify/$', UpdateEmailVerifyView.as_view(), name='user_update_email_verify'),
]
