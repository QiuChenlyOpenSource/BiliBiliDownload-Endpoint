# {"isLogin":true,"email_verified":1,"face":"https://i1.hdslb.com/bfs/face/ed2c9df24f653a59bbbff6c71afbc0505697187f.jpg","face_nft":0,"face_nft_type":0,"level_info":{"current_level":5,"current_min":10800,"current_exp":23920,"next_exp":28800},"mid":10525429,"mobile_verified":1,"money":1870,"moral":70,"official":{"role":0,"title":"","desc":"","type":-1},"officialVerify":{"type":-1,"desc":""},"pendant":{"pid":0,"name":"","image":"","expire":0,"image_enhance":"","image_enhance_frame":"","n_pid":0},"scores":0,"uname":"bili_8471246812","vipDueDate":1518624000000,"vipStatus":0,"vipType":1,"vip_pay_type":0,"vip_theme_type":0,"vip_label":{"path":"","text":"","label_theme":"","text_color":"","bg_style":0,"bg_color":"","border_color":"","use_img_label":true,"img_label_uri_hans":"","img_label_uri_hant":"","img_label_uri_hans_static":"https://i0.hdslb.com/bfs/vip/d7b702ef65a976b20ed854cbd04cb9e27341bb79.png","img_label_uri_hant_static":"https://i0.hdslb.com/bfs/activity-plat/static/20220614/e369244d0b14644f5e1a06431e22a4d5/KJunwh19T5.png"},"vip_avatar_subscript":0,"vip_nickname_color":"","vip":{"type":1,"status":0,"due_date":1518624000000,"vip_pay_type":0,"theme_type":0,"label":{"path":"","text":"","label_theme":"","text_color":"","bg_style":0,"bg_color":"","border_color":"","use_img_label":true,"img_label_uri_hans":"","img_label_uri_hant":"","img_label_uri_hans_static":"https://i0.hdslb.com/bfs/vip/d7b702ef65a976b20ed854cbd04cb9e27341bb79.png","img_label_uri_hant_static":"https://i0.hdslb.com/bfs/activity-plat/static/20220614/e369244d0b14644f5e1a06431e22a4d5/KJunwh19T5.png"},"avatar_subscript":0,"nickname_color":"","role":0,"avatar_subscript_url":"","tv_vip_status":0,"tv_vip_pay_type":0,"tv_due_date":0,"avatar_icon":{"icon_resource":{}}},"wallet":{"mid":10525429,"bcoin_balance":0,"coupon_balance":0,"coupon_due_time":0},"has_shop":false,"shop_url":"","allowance_count":0,"answer_status":0,"is_senior_member":0,"wbi_img":{"img_url":"https://i0.hdslb.com/bfs/wbi/7cd084941338484aae1ad9425b84077c.png","sub_url":"https://i0.hdslb.com/bfs/wbi/4932caff0ff746eab6f01bf08b70ac45.png"},"is_jury":false}
# 根据上面的json生成对应的数据库类

from tortoise.models import Model, DoesNotExist
from tortoise import fields


class UserInformationCache(Model):
    """生成一个UserInfomationCache模型

    Args:
        Model (任意字符串类型): 字符串
    """

    id = fields.IntField(pk=True)
    mid = fields.IntField()
    info = fields.CharField(max_length=5000)
    # 设置更新时自动更新为当前时间
    updated_at = fields.DatetimeField(auto_now_add=True)
