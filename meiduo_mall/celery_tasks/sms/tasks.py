#!/usr/bin/env python
# coding:utf-8
# Created by  on 18-12-23
# Copyright (c) 2018 $USER.ALL rights reserved.
import logging
from .utils.yuntongxun.sms import CCP
from ..main import app

logger = logging.getLogger('django')


@app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code, expires, temp_id):
    # 发送短信
    try:
        ccp = CCP()
        result = ccp.send_template_sms(mobile, [sms_code, expires], temp_id)
    except Exception as e:
        logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
        # return Response({'message': 'failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if result == 0:
            logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
            # return Response({'message': 'OK'})
        else:
            logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)
            # return Response({'message': 'failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)