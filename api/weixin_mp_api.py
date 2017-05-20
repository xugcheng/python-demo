#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
微信公众号api调用
'''

import httplib
import json
from context import G_CONTEXT

WEIXIN_API_HOST = 'api.weixin.qq.com'


class HttpMethod(object):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'
    PATCH = 'PATCH'
    TRACE = 'TRACE'


# 发送客服消息
def send_custom_msg(access_token, msg_body):
    custom_msg_uri = '/cgi-bin/message/custom/send?access_token=%s' % access_token
    conn = httplib.HTTPSConnection(WEIXIN_API_HOST)
    conn.request(HttpMethod.POST, custom_msg_uri, msg_body)
    response = conn.getresponse().read()
    conn.close()
    return response


if __name__ == '__main__':
    redis_client = G_CONTEXT.get_redis_client()
    wx_access_token = redis_client.get('WX_ACCESS_TOKEN')
    print 'access_token = ', wx_access_token

    open_id = 'ochATxDxsrR_UsguDSbmvOULNeLI'

    text_msg_body = {
        'touser': open_id,
        'msgtype': 'text',
        'text':
            {
                'content': '你好'
            }
    }

    result = send_custom_msg(wx_access_token, json.dumps(text_msg_body, ensure_ascii=False))

    print '发送文本消息:', result

    news_msg_body = {
        'touser': open_id,
        'msgtype': 'news',
        'news': {
            'articles': [
                {
                    'title': '学生1 学生已到校',
                    'description': '学生1已到校,请家长知悉',
                    'url': 'https://testschwxgz.icomwell.com/index.htm?push=true&studentId=%d' % 1,
                    'picurl': 'https://testschimg.icomwell.com/image/school/news-board6/sch11-by2-20170117111422-0.png'
                }
            ]
        }
    }

    result = send_custom_msg(wx_access_token, json.dumps(news_msg_body, ensure_ascii=False))

    print '发送图文消息:', result
