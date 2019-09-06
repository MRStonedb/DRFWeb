#!/usr/bin/env python
# coding:utf-8
# Created by  on 18-12-23
# Copyright (c) 2018 $USER.ALL rights reserved.
import logging
from rest_framework import serializers
from django_redis import get_redis_connection


logger = logging.getLogger('django')


class ImageCodeCheckSerializer(serializers.Serializer):
    """
    图片验证码校验序列化器,
    选择serializers.Serializer，是因为检验的参数不涉及model,
    经验：继承自那个类，需要看被校验的参数是否涉及数据库
    """
    image_code_id = serializers.UUIDField()
    text = serializers.CharField(max_length=4, min_length=4)

    def validate(self, attrs):
        """
        校验，选择validate_   是针对一个特定的字段
        选择validate   跨字段联合校验
        被校验的参数通过参数 attrs 取得
        """
        image_code_id = attrs.get('image_code_id', '')
        text = attrs.get('text', '')

        # 查询真实图片验证码
        redis_conn = get_redis_connection('verify_codes')
        real_image_code_text = redis_conn.get('img_%s' % image_code_id)
        if not real_image_code_text:
            raise serializers.ValidationError('图片验证码无效')

        # 删除图片验证码
        try:
            redis_conn.delete('img_%s' % image_code_id)
        except RedisError as e:
            logger.error(e)

        # 比较图片验证码
        real_image_code_text = real_image_code_text.decode()
        if real_image_code_text.lower() != text.lower():
            raise serializers.ValidationError('图片验证码错误')

        # 判断是否在60s内
        # get_serializer 方法在创建序列化器对象时，会补充context属性
        # context 属性中包含三个值： request  format   view 类视图对象
        # self.context['view'] 相当于  当前的view试图：即SMSCodeView 视图

        # django的类视图对象中，kwargs属性保存了路径提取出来的参数
        # kwargs['mobile'] 相当于 SMSCodeView 视图的路径参数 mobile
        mobile = self.context['view'].kwargs['mobile']
        send_flag = redis_conn.get("send_flag_%s" % mobile)
        if send_flag:
            raise serializers.ValidationError('请求次数过于频繁')

        return attrs