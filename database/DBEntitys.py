#  Copyright (c) 2023-2024. 秋城落叶, Inc. All Rights Reserved
#  @作者 : 秋城落叶(QiuChenly)
#  @邮件 : qiuchenly@outlook.com
#  @文件 : 项目 [BiliBiliApp] - DBEntitys.py by qiuchenly
#  @时间 : 2024/2/16 上午3:18
#

from tortoise.models import Model
from tortoise import fields


class UserConfig(Model):
    """生成一个UserConfig模型

    Args:
        Model (任意字符串类型): 字符串
    """

    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=255)
    value = fields.TextField()


class LoginSession(Model):
    """生成一个LoginSession模型

    Args:
        Model (任意字符串类型): 字符串
    """

    id = fields.IntField(pk=True)

    SESSDATA = fields.CharField(max_length=255)
    bili_jct = fields.CharField(max_length=255)
    DedeUserID = fields.CharField(max_length=255)
    DedeUserID__ckMd5 = fields.CharField(max_length=255)
    sid = fields.CharField(max_length=255)
