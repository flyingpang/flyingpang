# coding: utf-8

import sys
from django.views.debug import technical_500_response


class UserBasedExceptionMiddleware(object):

    """
    DEBUG=False,
    如果网站出现错误,普通用户看到的是报错信息,
    管理员看到的是错误详情,以便修复BUG
    """

    def process_exception(self, request):
        if request.user.is_admin:
            return technical_500_response(request, *sys.exc_info())
