#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import logging
from django.conf import settings
from urllib.parse import urlencode, parse_qs
import urllib.parse
from urllib.request import urlopen
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData

from .exceptions import QQAPIError
from  . import constants
 

logger = logging.getLogger('django')

class OAuthQQ(object):
    """
    qq认证辅助工具类
    """
    def __init__(self,client_secret=None, client_id=None, redirect_uri=None, state=None):
        self.client_id = client_id if client_id else settings.QQ_CLIENT_ID
        self.redirect_uri = redirect_uri if redirect_uri else settings.QQ_REDIRECT_URI
        self.state = state if state else settings.QQ_STATE  
        self.client_secret = client_secret if client_secret else settings.QQ_CLIENT_SECRET

    def get_login_url(self):
        url = 'https://graph.qq.com/oauth2.0/authorize?'

        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state
        }

        url += urllib.parse.urlencode(params)

        return url

    def get_access_token(self, code):
        """
        获取access_token
        :param code: qq提供的code
        :return: access_token
        """
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        url = 'https://graph.qq.com/oauth2.0/token?' + urlencode(params)
        try:
            response = urlopen(url)
            response_data = response.read().decode()
            data = parse_qs(response_data)
            access_token = data.get('access_token', None)
        except Exception as err:
            logger.error("{}".format(err))
        else:
            if not access_token:
                logger.error('code=%s msg=%s' % (data.get('code'), data.get('msg')))
                raise QQAPIError

            return access_token[0]


    def get_openid(self, access_token):
        """
        获取用户的openid
        :param access_token: qq提供的access_token
        :return: open_id
        """
        url = 'https://graph.qq.com/oauth2.0/me?access_token=' + access_token
        response = urlopen(url)
        response_data = response.read().decode()
        try:
            # 返回的数据 callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} )\n;
            data = json.loads(response_data[10:-4])
        except Exception:
            data = parse_qs(response_data)
            logger.error('code=%s msg=%s' % (data.get('code'), data.get('msg')))
            raise QQAPIError
        openid = data.get('openid', None)
        return openid

    @staticmethod
    def generate_save_user_token(openid):
        """
        生成保存用户数据的token
        :param openid: 用户的openid
        :return: token
        """
        serializer = Serializer(settings.SECRET_KEY, expires_in=constants.SAVE_QQ_USER_TOKEN_EXPIRES)
        data = {'openid': openid}
        token = serializer.dumps(data)
        return token.decode()

    @staticmethod
    def check_save_user_token(token):
        """
        检验保存用户数据的token
        :param token: token
        :return: openid or None
        """
        serializer = Serializer(settings.SECRET_KEY, expires_in=constants.SAVE_QQ_USER_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return None
        else:
            return data.get('openid')