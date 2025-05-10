import logging
from functools import lru_cache

import requests
from typing import Dict, List

# 假设 QWEATHER_KEY 已定义在项目配置中
from myapi.settings.constants import QWEATHER_KEY,API_HOST

logger = logging.getLogger(__name__)

address_id = {
    "银川": "101170101",
    "吴忠": "101170301",
    "固原": "101170401",
    "中卫": "101170501",
    "石嘴山": "101170201",

}

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
class QWeatherService:
    def __init__(self, address: str):
        self.address = address
        self.key = QWEATHER_KEY
        self.api_host = API_HOST
        self.location_id = self._get_location_id()
        self.now_info = self._get_weather_now()

    @lru_cache(maxsize=128)
    def _get_location_id(self) ->  str:
        """获取地理位置ID"""
        if self.address  in address_id:
            return address_id[self.address]
        # 如果以后要拓展地图就这样但是就是有点浪费资源
        url = f"https://{self.api_host}/geo/v2/city/lookup/?location={self.address}&amd=银川&key={self.key}"
        try:
            response = requests.get(url)
        except requests.RequestException as e:
            logger.error("地理编码请求失败", exc_info=True)
            raise GeocodeError(f"网络请求失败：{e}") from e

        if response.status_code != 200:
            logger.warning("地理编码API返回非200状态码：%s", response.status_code)
            raise GeocodeError("地理编码API请求失败")
        data = response.json()
        if not data.get("location"):
            logger.warning("未获取到地理位置数据：%s", data)
            raise GeocodeError("未获取到地理位置数据")

        for loc in data["location"]:
            if loc["name"] == self.address:
                return loc["id"]

        logger.warning("未找到匹配的地址ID：%s", self.address)
        raise GeocodeError(f"未找到对应的城市ID：{self.address}")

    def _get_weather_now(self) -> Dict:
        url = f"https://{self.api_host}/v7/weather/now?location={self.location_id}&key={self.key}"

        try:
            response = requests.get(url)
        except requests.RequestException as e:
            logger.error("实时天气信息请求失败", exc_info=True)
            raise WeatherBaseError(f"网络请求失败：{e}") from e

        if response.status_code != 200:
            logger.warning("实时天气API返回非200状态码：%s", response.status_code)
            raise WeatherBaseError("实时天气信息请求失败")

        data = response.json()
        if not data.get("now"):
            logger.warning("未获取到实时天气数据：%s", data)
            raise WeatherBaseError("未获取到实时天气数据")

        return data["now"]

    def _get_weather_forecast(self,days: int = 3) -> List[Dict]:
        url = f"https://{self.api_host}/v7/weather/{days}d?location={self.location_id}&key={self.key}&days=3"

        try:
            response = requests.get(url)
        except requests.RequestException as e:
            logger.error("天气预报信息请求失败", exc_info=True)
            raise WeatherForecastError(f"网络请求失败：{e}") from e

        if response.status_code != 200:
            logger.warning("天气预报API返回非200状态码：%s", response.status_code)
            raise WeatherForecastError("天气预报信息请求失败")

        data = response.json()
        if not data.get("daily"):
            logger.warning("未获取到天气预报数据：%s", data)
            raise WeatherForecastError("未获取到天气预报数据")

        return data["daily"]

    def get_current_weather(self) -> Dict:
        return {
            "city": self.address,
            "temperature": self.now_info["temp"],
            "feels_like": self.now_info["feelsLike"],
            "weather": self.now_info["text"],
            "humidity": self.now_info["humidity"],
            "precipitation": self.now_info["precip"],  # 降水量
            "pressure": self.now_info["pressure"],  # 气压
            "windspeed": self.now_info["windSpeed"],
        }

    def get_forecast_weather(self,days: int = 3) -> List[Dict]:
        forecasts = []
        for day in self._get_weather_forecast(days):
            forecasts.append({
                "city": self.address,
                "date": day["fxDate"],
                "temp_max": float(day["tempMax"]),
                "temp_min": float(day["tempMin"]),
                "precip ": day["precip"],
                "sunset": day["sunset"],
                "windSpeedDay": day["windSpeedDay"],
                "windSpeedNight": day["windSpeedNight"],
                "humidity":  day["humidity"],
                "pressure": day["pressure"],
            })
        return forecasts

    @staticmethod
    def get_weather_info(address: str, choose: int = 3,days: int = 3) -> dict:
        try:
            instance = QWeatherService(address)
            data = {}
            if choose == 1:
                data["current"] = instance.get_current_weather()
            elif choose == 2:
                data["forecast"] = instance.get_forecast_weather(days)
            else:
                data["current"] = instance.get_current_weather()
                data["forecast"] = instance.get_forecast_weather(days)

            return data
        except WeatherServiceException as e:
            logger.error("获取天气信息失败：%s", str(e))
            return {"error": str(e)}
        except Exception as e:
            logger.exception("未知错误")
            return {"error": f"未知错误：{str(e)}"}


if __name__ == '__main__':
    cities = ["银川", "吴忠", "固原"]
    for city in cities:
        result = QWeatherService.get_weather_info(city, 2,7)
        print(result)
