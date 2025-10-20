from django.db import models
from crop.models import Growth
from myapi.utils.models import BaseModel

# Create your models here.
class DisasterJudgment(BaseModel):
    """灾情模型"""
    Growth_Disaster = models.ForeignKey(
        Growth,
        related_name="disaster_judgments",
        on_delete=models.PROTECT,
        verbose_name="所属作物生长周期",
        null=True,
        blank=True,
        db_index=True  # 添加索引
    )
    time_scope = models.CharField(
        verbose_name="时间范围",
        null=True,
        blank=True,
        help_text="存储不同类型灾害的时间范围",
        max_length=64,
    )
    name = models.CharField(max_length=64, verbose_name="灾情名称",db_index=True)
    detail_crop_type = models.CharField(max_length=64, verbose_name="所属具体的作物类型",null=True,blank=True,help_text="用于记录品种信息（如'巨峰葡萄'）")
    detail_growth_name = models.CharField(max_length=64, verbose_name="所属作物详细生长周期名称",null=True,blank=True,help_text="品种特有的生长阶段（如'赤霞珠转色期'）" )
    description = models.TextField(verbose_name="灾情描述", null=True, blank=True)
    formula_parameters = models.ManyToManyField(
        "DisasterParameter",
        verbose_name="公式参数",
        related_name="judgment_parameters",
        help_text="选择公式中使用的气象参数"
    )
    formula = models.TextField(verbose_name="灾情公式", null=True, blank=True,
                               help_text="python表达式，使用DisasterParameter中的参数")
    emergency_measure = models.TextField(verbose_name="应急措施", null=True, blank=True)
    disaster_type = models.ForeignKey(
        "DisasterType",
        on_delete=models.PROTECT,
        verbose_name="灾害类型",
        null=True,
        blank=True
    )
    disaster_level = models.ForeignKey(
        "DisasterLevel",
        on_delete=models.PROTECT,
        verbose_name="灾害等级",
        related_name="judgments",
        null=True,
        blank=True,

    )
    class Meta:
        db_table = "xm_disaster_judgment"
        verbose_name = "灾害"
        verbose_name_plural = "灾害"

    def __str__(self):
        return f"{self.detail_crop_type} - {self.name}"



class DisasterType(BaseModel):
    """灾情类型模型"""
    name = models.CharField(max_length=64, verbose_name="类型名称")
    description = models.TextField(verbose_name="类型描述", null=True, blank=True)

    class Meta:
        db_table = "xm_disaster_type"
        verbose_name = "灾害类型"
        verbose_name_plural = "灾害类型"


    def __str__(self):
        return self.name


class DisasterLevel(BaseModel):
    """灾害等级模型"""
    disaster_type = models.ForeignKey(
        DisasterType,
        on_delete=models.CASCADE,
        verbose_name="关联灾害类型"
    )
    level_name = models.CharField(max_length=32, verbose_name="等级名称",db_index=True)
    description = models.TextField(verbose_name="等级描述", null=True, blank=True)


    class Meta:
        db_table = "xm_disaster_level"
        verbose_name = "灾害等级"
        verbose_name_plural = "灾害等级"

    def __str__(self):
        return f"{self.disaster_type} - {self.level_name}"


class DisasterParameter(BaseModel):
    """可被引用的气象参数字典"""
    name = models.CharField(max_length=32, verbose_name="参数名称",db_index=True)

    class Meta:
        db_table = "xm_disaster_parameter"
        verbose_name = "气象参数"
        verbose_name_plural = "气象参数"

    def __str__(self):
        return self.name
