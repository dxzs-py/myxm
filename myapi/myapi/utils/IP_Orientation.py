import requests
from myapi.settings.constants import ORIENTATION
import logging

logger = logging.getLogger("django")

class IPLocationService:
    def __init__(self,coor="bd09ll"):
        self.api_url = "https://api.map.baidu.com/location/ip"
        self.ak = ORIENTATION
        self.coor = coor

    def get_location_by_ip(self, ip="1.50.37.255"):
        """通过IP地址获取地理位置信息

        Args:
            ip (str): 用户IP地址

        Returns:
            dict: 包含地理位置信息的字典
        """
        try:
            params = {
                "ip": ip,
                "coor": self.coor,
                "ak": self.ak
            }

            response = requests.get(url=self.api_url, params=params)
            # response.raise_for_status()  # 检查请求是否成功

            return response.json()

        except requests.RequestException as e:
            logger.error(f"IP定位请求失败: {str(e)}")
            return {"error": "定位服务不可用"}
        except Exception as e:
            logger.error(f"IP定位处理失败: {str(e)}")
            return {"error": "定位处理异常"}

if __name__ == '__main__':
    ip_service = IPLocationService()
    location = ip_service.get_location_by_ip()
    print(location)
