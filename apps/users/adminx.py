import xadmin
import xadmin.views

from .models import EmailVerifyRecord, Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSetting(object):
    site_title = '旺财学习平台'
    site_footer = '旺财版权所有'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['id', 'code', 'address', 'send_type', 'send_time']
    search_fields = ['code', 'address', 'send_type']
    list_filter = ['code', 'address', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)
xadmin.site.register(xadmin.views.CommAdminView, GlobalSetting)
