"""这里存放一些默认常量，统一管理"""

# 设置效果常量，增加可读性
BANNER_LENGTH = 5  # 轮播图数量

HEADER_NAV_LENGTH = 8  # 头部导航数量

FOOTER_NAV_LENGTH = 8  # 底部导航数量

# 短信的有效期[单位：秒]
SMS_EXPIRE_TIME = 60 * 4

# 短信的时间间隔[单位：秒]
SMS_INTERVAL_TIME = 60

# 短信的模版id，测试开发时使用 1
SMS_TEMPLATE_ID = 1

GWEATHER_KEY = "dbe67ecd6987dfaa3d98fbd4b454793c"

QWEATHER_KEY = "02e8d7ad5e39436eb62ccbbd05df7081"

API_HOST = "p64ewr8ayt.re.qweatherapi.com"

HOST = "http://www.mtl.cn:8000"

TIME_ZONE = 'Asia/Shanghai'

import datetime
import pytz

# UTC时区对象
UTC_TZ = datetime.timezone.utc

# 北京时间时区对象
BEIJING_TZ = pytz.timezone(TIME_ZONE)

POSTPONE_THE_YEAR = 3

SIGNATURE = """
-----BEGIN PRIVATE KEY-----
MC4CAQAwBQYDK2VwBCIEILgit6Ws/W9QQ7IMZ7BQnT9Ou14fA/EKnhYIlDcpSVbR
-----END PRIVATE KEY-----
"""

PROOF_ID = "TKGU67RKN8"

SUB = "3GDYB4XQRE"

URGENCY = {
    "immediate": "必须立刻采取行动",
    "expected": "应尽快采取行动（通常在 1 小时内）",
    "future": "应在近期采取行动",
    "past": "事件已不再发生",
    "unknown": "紧迫性未知",
}
SEVERITY = {
    "minor": "对生命或财产构成的威胁极小或没有已知威胁",
    "moderate": "对生命或财产可能构成威胁",
    "severe": "对生命或财产构成的重大威胁",
    "unknown": "严重性未知",
    "extreme": "对生命或财产构成的严重威胁",
}
CERTAINTY = {
    "likely": "发生概率大于约 50%",
    "unlikely": "预计不会发生（概率接近 0）",
    "unknown": "确定性未知",
    "possible": "有可能发生，但概率较低（≤ 50%）",
    "observed": "事件已经发生或正在发生"
}

ORIENTATION = "agqae7zVleUZIAZbUH4ifILrLcykDbgz"
