# -*- coding: utf-8 -*-
"""
自定义中间件，用于修改或移除安全头
"""

from django.utils.deprecation import MiddlewareMixin


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    处理安全头的中间件
    """
    
    def process_response(self, request, response):
        # 移除Cross-Origin-Opener-Policy头，解决开发环境中的警告
        if 'Cross-Origin-Opener-Policy' in response:
            del response['Cross-Origin-Opener-Policy']
        
        # 确保没有设置这个头
        if hasattr(response, '_headers'):
            headers = list(response._headers.keys())
            for header in headers:
                if header.lower() == 'cross-origin-opener-policy':
                    del response._headers[header]
        
        return response