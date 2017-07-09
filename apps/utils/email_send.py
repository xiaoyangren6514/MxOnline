import random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


def generate_random_str(length=8):
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(length):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


def send_register_email(email, type='register'):
    email_record = EmailVerifyRecord()
    email_record.code = generate_random_str(16)
    email_record.send_type = type
    email_record.address = email
    email_record.save()

    email_title = ''
    email_content = ''

    if type == 'register':
        email_title = '猪八戒背媳妇网站注册邮件'
        email_content = '欢迎注册，请点击以下链接完成注册:http://127.0.0.1:8000/active/{0}'.format(email_record.code)
        status = send_mail(email_title, email_content, EMAIL_FROM, [email])
        if status:
            pass
    elif type == 'forget':
        email_title = '猪八戒背媳妇网站忘记密码邮件'
        email_content = '欢迎注册，请点击以下链接完成注册:http://127.0.0.1:8000/reset/{0}'.format(email_record.code)
        status = send_mail(email_title, email_content, EMAIL_FROM, [email])
        if status:
            pass
    elif type == 'update_email':
        email_title = '猪八戒背媳妇网站修改邮箱邮件'
        email_content = '欢迎修改邮箱，请点击以下链接完成注册:http://127.0.0.1:8000/user/update/email/verify/{0}'.format(
            email_record.code)
        status = send_mail(email_title, email_content, EMAIL_FROM, [email])
        if status:
            pass
