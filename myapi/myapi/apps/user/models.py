from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.exceptions import ValidationError

from myapi.utils.models import BaseModel


class User(AbstractUser):
    # 自定义字段
    mobile = models.CharField(max_length=15, unique=True, verbose_name="手机号", db_index=True, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True, verbose_name="用户头像")
    wechat = models.CharField(max_length=64, null=True, blank=True, verbose_name="微信号")
    city = models.ForeignKey(
        "City",
        related_name="city_user",
        on_delete=models.SET_NULL,  # 更安全的选项，删除城市时不会删除用户
        verbose_name="城市",
        null=True,
        blank=True
    )
    county = models.ForeignKey(
        "County",
        related_name="county_user",
        on_delete=models.SET_NULL,  # 更安全的选项，删除县时不会删除用户
        verbose_name="县",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "xm_users"
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        返回用户的完整信息
        """
        full_info = [self.username]
        if self.city:
            full_info.append(self.city.name)
        if self.county:
            full_info.append(self.county.name)
        return " - ".join(full_info)

    def clean(self):
        # 验证county必须属于指定的city
        if self.city and self.county and self.county.city_belong != self.city:
            raise ValidationError("所选县必须属于指定城市")
        # 如果提供了手机号，验证手机号格式
        if self.mobile:
            import re
            if not re.match(r'^1[3-9]\d{9}$', self.mobile):
                raise ValidationError({"mobile": "请输入有效的手机号码"})

    def save(self, *args, **kwargs):
        # 在保存前进行验证
        self.full_clean()
        super().save(*args, **kwargs)


class County(BaseModel):
    name = models.CharField(max_length=64, verbose_name="名称")
    city_belong = models.ForeignKey(
        "City",
        related_name="city_county",
        on_delete=models.PROTECT,
        verbose_name="所属城市",
    )

    class Meta:
        db_table = "xm_county"
        verbose_name = "县"
        verbose_name_plural = "县"

    def __str__(self):
        return f"{self.city_belong.name} - {self.name}"


class City(BaseModel):
    """城市模型"""
    name = models.CharField(max_length=64, verbose_name="城市名称", unique=True)
    province = models.ForeignKey(
        "Province",
        related_name="province_city",
        on_delete=models.PROTECT,
        verbose_name="所属省",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "xm_city"
        verbose_name = "城市"
        verbose_name_plural = "城市"

    def __str__(self):
        return self.name

class Province(BaseModel):
    """省模型"""
    name = models.CharField(max_length=64, verbose_name="省名称", unique=True)

    class Meta:
        db_table = "xm_province"
        verbose_name = "省"
        verbose_name_plural = "省"

    def __str__(self):
        return self.name