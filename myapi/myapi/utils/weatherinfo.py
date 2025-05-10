import json
import logging
import requests
from functools import lru_cache
from typing import Dict, List

# 假设 WEATHER_KEY 已定义在项目配置中
from myapi.settings.constants import GWEATHER_KEY

logger = logging.getLogger(__name__)


# ========== 异常定义 ==========
class WeatherServiceException(Exception):
    """天气服务基类异常"""
    pass


class GeocodeError(WeatherServiceException):
    """地理编码失败"""
    pass


class WeatherBaseError(WeatherServiceException):
    """获取当前天气失败"""
    pass


class WeatherForecastError(WeatherServiceException):
    """获取预报信息失败"""
    pass


# ========== 天气服务主类 ==========
class GaoDeWeatherService:
    def __init__(self, address: str):
        self.address = address
        self.key = GWEATHER_KEY
        self.adcode = self._get_adcode()
        self.city_info = self._get_weather_base()
        self.forecast_info = self._get_weather_forecast()

    @lru_cache(maxsize=128)
    def _get_adcode(self) -> str:
        url = f"https://restapi.amap.com/v5/geocode/geo?address={self.address}&key={self.key}"

        try:
            response = requests.get(url)
        except requests.RequestException as e:
            logger.error("地理编码请求失败", exc_info=True)
            raise GeocodeError(f"网络请求失败：{e}") from e

        if response.status_code != 200:
            logger.warning("地理编码API返回非200状态码：%s", response.status_code)
            raise GeocodeError("地理编码API请求失败")

        data = response.json()
        if "geocodes" not in data or not data["geocodes"]:
            logger.warning("地理编码无有效数据：%s", data)
            raise GeocodeError(f"地理编码失败，返回数据：{data}")

        return data["geocodes"][0]["adcode"]

    def _get_weather_base(self) -> Dict:
        url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={self.key}&city={self.adcode}&extensions=base&output=JSON"

        try:
            response = requests.get(url)
        except requests.RequestException as e:
            logger.error("基础天气信息请求失败", exc_info=True)
            raise WeatherBaseError(f"网络请求失败：{e}") from e

        if response.status_code != 200:
            logger.warning("基础天气信息API返回非200状态码：%s", response.status_code)
            raise WeatherBaseError("天气基础信息请求失败")

        data = response.json()
        if not data.get("lives"):
            logger.warning("未获取到基础天气数据：%s", data)
            raise WeatherBaseError("未获取到天气基础数据")

        return data["lives"][0]

    def _get_weather_forecast(self) -> List[Dict]:
        url = f"https://restapi.amap.com/v3/weather/weatherInfo?key={self.key}&city={self.adcode}&extensions=all&output=JSON"

        try:
            response = requests.get(url)
        except requests.RequestException as e:
            logger.error("天气预报信息请求失败", exc_info=True)
            raise WeatherForecastError(f"网络请求失败：{e}") from e

        if response.status_code != 200:
            logger.warning("天气预报API返回非200状态码：%s", response.status_code)
            raise WeatherForecastError("天气预报信息请求失败")

        data = response.json()
        if not data.get("forecasts") or not data["forecasts"][0].get("casts"):
            logger.warning("未获取到天气预报数据：%s", data)
            raise WeatherForecastError("未获取到天气预报数据")

        return data["forecasts"][0]["casts"]

    def get_current_weather(self) -> Dict:
        return {
            "city": self.city_info["city"],
            "temperature": self.city_info["temperature"],
            "weather": self.city_info["weather"],
            "humidity": self.city_info["humidity"],
            "winddirection": self.city_info["winddirection"],
            "windpower": self.city_info["windpower"],
            "reporttime": self.city_info["reporttime"]
        }

    def get_forecast_weather(self) -> List[Dict]:
        return self.forecast_info

    @staticmethod
    def get_weather_info(address: str,choose:int = 3) -> dict:
        try:
            instance = GaoDeWeatherService(address)
            data = {}
            if choose==1:
                data["current"] = instance.get_current_weather()
            elif choose==2:
                data["forecast"] = instance.get_forecast_weather()
            else:
                data["current"] = instance.get_current_weather()
                data["forecast"] = instance.get_forecast_weather()

            return data
        except WeatherServiceException as e:
            logger.error("获取天气信息失败：%s", str(e))
            return {"error": str(e)}
        except Exception as e:
            logger.exception("未知错误")
            return {"error": f"未知错误：{str(e)}"}


# ========== 主函数测试逻辑（建议迁移到测试模块） ==========
if __name__ == '__main__':
    cities = ["银川", "吴忠市", "固原市"]
    for city in cities:
        result = json.dumps(GaoDeWeatherService.get_weather_info(city,1), ensure_ascii=False, indent=2)
        print(result)
